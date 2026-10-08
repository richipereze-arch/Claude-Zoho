import json
import tempfile
import unittest
from pathlib import Path

from zoho_loader import normalize as n, dedup, pipeline
from zoho_loader.schema import Schema, mask

FIX = Path(__file__).parent / "fixtures"


class NormalizeTest(unittest.TestCase):
    def test_phone(self):
        self.assertEqual(n.phone_cl("9 8765 4321")[0], "+56987654321")
        self.assertEqual(n.phone_cl("56987654321")[0], "+56987654321")
        self.assertEqual(n.phone_cl("+56 2 2345 6789")[0], "+56223456789")
        self.assertIsNone(n.phone_cl("87654321")[0])  # ambiguo: no se completa
        self.assertEqual(n.phone_cl("+1 415 555 0100")[0], "+14155550100")

    def test_email(self):
        self.assertEqual(n.email(" Juan.Perez@Example.com ")[0], "juan.perez@example.com")
        self.assertIsNone(n.email("maria@example")[0])

    def test_rut(self):
        self.assertEqual(n.rut("11111111-1")[0], "11.111.111-1")
        self.assertEqual(n.rut("12.345.678-5")[0], "12.345.678-5")
        self.assertIsNotNone(n.rut("12345678-9")[1])

    def test_dates_amounts(self):
        self.assertEqual(n.date_iso("05/03/2026")[0], "2026-03-05")
        self.assertEqual(n.amount("$1.234.567")[0], 1234567.0)
        self.assertEqual(n.amount("1.234,50")[0], 1234.5)
        self.assertEqual(n.amount("USD 1,500.25")[0], 1500.25)
        self.assertIsNotNone(n.currency("EUR")[1])

    def test_company_key(self):
        self.assertEqual(n.company_key("Inversiones Ñuñoa SpA"), n.company_key("INVERSIONES ÑUÑOA S.p.A."))
        self.assertEqual(n.company_key("Rojas Ltda."), "rojas")


class SchemaTest(unittest.TestCase):
    def test_mandatory_and_picklist(self):
        s = Schema("Leads")
        self.assertIn("Last_Name", s.mandatory())
        self.assertIn("Company", s.mandatory())
        rec = {"Last_Name": "X", "Company": "Y", "Producto": "leaseback", "Lead_Status": "Contacted"}
        self.assertEqual(s.validate(rec), [])
        self.assertEqual(rec["Producto"], "Leaseback")
        self.assertEqual(rec["Lead_Status"], "Contactado")
        self.assertTrue(any("no permitido" in i for i in s.validate({"Last_Name": "X", "Company": "Y", "Producto": "Cripto"})))

    def test_accounts_requires_rut_by_layout(self):
        self.assertIn("RUT", Schema("Accounts").mandatory())

    def test_mask(self):
        self.assertEqual(mask("RUT", "12.345.678-5"), "***8-5")
        self.assertTrue(mask("Email", "juan@example.com").startswith("ju***@"))


class DedupTest(unittest.TestCase):
    def test_email_match_is_existing(self):
        r = dedup.classify("Leads", {"Email": "a@b.cl", "Last_Name": "Ana"},
                           [{"id": "1", "Email": "A@b.cl", "Last_Name": "Ana", "_module": "Leads"}])
        self.assertEqual(r["status"], dedup.EXISTING)

    def test_phone_only_is_possible(self):
        r = dedup.classify("Leads", {"Mobile": "+56987654321", "Last_Name": "Ana Soto"},
                           [{"id": "1", "Mobile": "987654321", "Last_Name": "Pedro Pérez", "_module": "Leads"}])
        self.assertEqual(r["status"], dedup.POSSIBLE)

    def test_two_strong_is_ambiguous(self):
        r = dedup.classify("Leads", {"Email": "a@b.cl"},
                           [{"id": "1", "Email": "a@b.cl", "_module": "Leads"}, {"id": "2", "Email": "a@b.cl", "_module": "Leads"}])
        self.assertEqual(r["status"], dedup.AMBIGUOUS)

    def test_contact_existing_flags_lead(self):
        r = dedup.classify("Leads", {"Email": "a@b.cl"}, [{"id": "9", "Email": "a@b.cl", "_module": "Contacts"}])
        self.assertEqual(r["status"], dedup.POSSIBLE)

    def test_merge_never_overwrites(self):
        upd, conf = dedup.merge_update({"Email": "a@b.cl", "Producto": "Mutuo", "Owner": {"id": "2"}},
                                       {"Email": None, "Producto": "Trading", "Owner": {"id": "1"}})
        self.assertEqual(upd, {"Email": "a@b.cl"})
        self.assertEqual(conf[0]["field"], "Producto")


class PipelineTest(unittest.TestCase):
    def test_end_to_end_dry_run(self):
        with tempfile.TemporaryDirectory() as d:
            meta, rows = pipeline.plan("Leads", FIX / "leads_ejemplo.csv", "test", d, defaults={"Lead_Source": "Aviso"})
            self.assertIn("Columna X", meta["unmapped_columns"])
            self.assertEqual(rows[0]["record"]["Mobile"], "+56987654321")
            self.assertEqual(rows[0]["record"]["Last_Name"], "Juan Pérez Soto")
            self.assertEqual(rows[0]["provenance"]["Lead_Source"], "instrucción")
            self.assertTrue(any("Company" in i for i in rows[1]["issues"]))
            self.assertTrue(any("no permitido" in i for i in rows[2]["issues"]))
            cand = {rows[0]["row_key"]: []}
            Path(d, "c.json").write_text(json.dumps(cand))
            planned = pipeline.classify(d, Path(d, "c.json"))
            acts = [r["action"] for r in planned["rows"]]
            self.assertEqual(acts, ["crear", "error", "error"])
            self.assertEqual(len(planned["chunks"]), 1)
            resp = {"data": [{"status": "success", "code": "SUCCESS", "details": {"id": "555"}, "message": "ok"}]}
            Path(d, "r.json").write_text(json.dumps(resp))
            done = pipeline.record(d, 1, Path(d, "r.json"))
            self.assertEqual(len(done), 1)
            # reanudable: al reclasificar, la fila ya creada se omite
            planned = pipeline.classify(d, Path(d, "c.json"))
            self.assertEqual(planned["rows"][0]["action"], "omitir")
            payload = json.loads(Path(d, "plan.json").read_text())
            fetched = {"555": dict(rows[0]["record"])}
            Path(d, "f.json").write_text(json.dumps(fetched))
            self.assertEqual(pipeline.verify(d, Path(d, "f.json")), [])


if __name__ == "__main__":
    unittest.main()
