# 02 · Diccionario de datos — Zoho CRM (Banca Inversiones)

Generado automáticamente por `tools/build_dictionary.py` desde la metadata real (`getFields` + `getLayouts`) vía el conector MCP oficial. Solo metadata: no contiene registros.

Leyenda *Oblig.*: **S** = obligatorio de sistema, **L** = obligatorio por layout, vacío = opcional.

## Leads

Layouts: Standard (`6839037000000091055`, active)

| Campo visible | API name | Tipo | Oblig. | Valores permitidos | Observaciones |
|---|---|---|---|---|---|
| Nombre Completo | `Last_Name` | text | S |  | Obligatorio de sistema |
| Nombre Cuenta | `Company` | text | L |  | Obligatorio por layout |
| Analista de Inversiones | `Analista_de_Inversiones` | picklist |  | Lucas Justiniano; Camilo Bravo; Jose Quevedo; Diego Vargas; Hari Saits; Marcelo Henandez; Ricardo Perez; Camila Jofre; David Gomez | Personalizado |
| Atributo del Prospecto | `Atributo_del_Prospecto` | picklist |  | Interesado; Diferido; Archivado; No Interesado; No Califica; No Ubicable; Marketing; Broker; Teléfono Malo; Proceso de Cierre; Desistio; Enviar Simulación; Simulación Enviada; Recopilación de documentos; Presentar a comité; Comité aprueba - EETT; Comité no aprueba; Enviado a EETT; Borradores Listos; Firmado; Inbound; Monto Menor; Sin Tasación Comercial | Personalizado |
| Broker FK | `Broker_FK` | picklist |  | Abel Cancino Asesor; Alejandra Madrid Martinez Asesor; Alejandro Vielma Asesor; Alexis Garrido Asesor; Alexis Muñoz Medina Asesor; Andres Alejandro Bilbao Pozo; Angelica Medina Asesora; Angelina Zuñiga Asesora; Bernardita Pizarrón Asesora; Carlos Godoy Guajardo Asesor; Carlos Javier Barria; Carlos Olguin; Carolina Nallar; Carolina Soto; Christian Tampe Asesor; Christopher Díaz Suarez Asesor; Claudia Saldaña Asesora; Cristian Fonseca Asesor; Daniel Heinrich Asesor; Dannette Ordoñez Henriquez; David Ocaranza Asesor; Esteban Retamal Santibañez; Fabian Valenzuela Asesor; Gabriela Soto Asesora; Godfrey Dawson; Gonzalo Moyano Asesor Comercial; Gonzalo Risso Asesores; Jaime Sandoval Asesor; Javier Bunster; Javiera Perez Valdes Asesor; Jesus Cruces Palma; Jorge Castillo; Jorge Yanez Mardonez Asesor; José Luis Cifuentes Martinez Asesor M; José Luis Jiménez Orellana Asesor; Jose Luis Muñoz Asesor; José Padilla Asesor; Jose Saez; Juan Elgueta Asesor; Juan Enrique Urquhart Asesor; Karen Inostroza Asesora; Kenita Moya Asesora; León Vidal Asesor; Leonardo Medina M&M Asesor; Lionel Rubio Aceituno; Luckas Ortiz; Luis Cabrera Retamal Asesor; Luis Correa Asesor; Luis Hidalgo Asesor; Manuel González Asesor; Marcelo James Harmitton; Marcelo Mocelli Asesor; Marco Antonio Ureta Asesor ✍️????; Marco Cornejo Asesor; Marcos Ponce Asesor; Maria Angelica Pérez Gallardo Asesora; Maria Susana Salazar Jara Asesora Financiak; Mauricio Arancibia Rojas Asesor; Mauricio Coloma Asesor; Mauricio Pérez Celedon Asesor; Mauro Escobar Salgado; Oliver Diaz; Pablo Castro Asesor; Pablo Mercado Asesor; Pablo Solís J.; Paola Rodríguez Fuentes Asesora; Paola Rojas Asesora; Patricio Caceres ®️ asesor Pinilla ®️; Patricio Herrera Asesor; Patricio Nuñez Asesor; Paulina Ninoska Nuñez Asesora; Renato Eugenio Ezquerro carrillo Asesor; Richard Morales Asesor; Rita Solange Castro Gonzalez Asesor; Roberto Fuentes Ramirez Asesor; Roberto González Caceres Asesor; Rodrigo Garrido Alvear Asesor; Rosa Irene Basualto Yañez; Sandra Dueñas Riffo Asesora; Sebastián de Rementería Asesor; Sebastian Valenzuela Gil; Sergio Arcos Illanes Asesor; Victor Perez Cid Asesor; Virginia Contreras | Personalizado |
| Comuna / Ciudad | `Comuna_Ciudad` | picklist |  | Alto Hospicio; Iquique; Huara; Camiña; Colchane; Pica; Pozo Almonte; Tocopilla; María Elena; Calama; Ollagüe; San Pedro de Atacama; Antofagasta; Mejillones; Sierra Gorda; Taltal; Chañaral; Diego de Almagro; Copiapó; Caldera; Tierra Amarilla; Vallenar; Freirina; Huasco; Alto del Carmen; La Serena; La Higuera; Coquimbo; Andacollo; Vicuña; Paihuano; Ovalle; Río Hurtado; Monte Patria; Combarbalá; Punitaqui; Illapel; Salamanca; Los Vilos; Canela; La Ligua; Petorca; Cabildo; Zapallar; Papudo; Los Andes; San Esteban; Calle Larga; Rinconada; San Felipe; Putaendo; Santa María; Panquehue; Llaillay; Catemu; Quillota; La Cruz; Calera; Nogales; Hijuelas; Limache; Olmué; Valparaíso; Viña del Mar; Quintero; Puchuncaví; Quilpué; Villa Alemana; Casablanca; Concón; Juan Fernández; San Antonio; Cartagena; El Tabo; El Quisco; Algarrobo; Santo Domingo; Isla de Pascua; Rancagua; Graneros; Mostazal; Codegua; Machalí; Olivar; Requinoa; Rengo; Malloa; Quinta de Tilcoco; San Vicente; Pichidegua; Peumo; Coltauco; Coinco; Doñihue; Las Cabras; San Fernando; Chimbarongo; Placilla; Nancagua; Chépica; Santa Cruz; Lolol; Pumanque; Palmilla; Peralillo; Pichilemu; Navidad; Litueche; La Estrella; Marchihue; Paredones; Curicó; Teno; Romeral; Molina; Sagrada Familia; Hualañé; Licantén; Vichuquén; Rauco; Talca; Pelarco; Río Claro; San Clemente; Maule; San Rafael; Empedrado; Pencahue; Constitución; Curepto; Linares; Yerbas Buenas; Colbún; Longaví; Parral; Retiro; Villa Alegre; San Javier; Cauquenes; Pelluhue; Chanco; Chillán; San Carlos; Ñiquén; San Fabián; Coihueco; Pinto; San Ignacio; El Carmen; Yungay; Pemuco; Bulnes; Quillón; Ránquil; Portezuelo; Coelemu; Treguaco; Cobquecura; Quirihue; Ninhue; San Nicolás; Chillán Viejo; Alto Biobío; Los Angeles; Cabrero; Tucapel; Antuco; Quilleco; Santa Bárbara; Quilaco; Mulchén; Negrete; Nacimiento; Laja; San Rosendo; Yumbel; Concepción; Talcahuano; Penco; Tomé; Florida; Hualpén; Hualqui; Santa Juana; Lota; Coronel; San Pedro de la Paz; Chiguayante; Lebu; Arauco; Curanilahue; Los Alamos; Cañete; Contulmo; Tirua; Angol; Renaico; Collipulli; Lonquimay; Curacautín; Ercilla; Victoria; Traiguén; Lumaco; Purén; Los Sauces; Temuco; Lautaro; Perquenco; Vilcún; Cholchol; Cunco; Melipeuco; Curarrehue; Pucón; Villarrica; Freire; Pitrufquén; Gorbea; Loncoche; Toltén; Teodoro Schmidt; Saavedra; Carahue; Nueva Imperial; Galvarino; Padre las Casas; Valdivia; Mariquina; Lanco; Máfil; Corral; Los Lagos; Panguipulli; Paillaco; La Unión; Futrono; Río Bueno; Lago Ranco; Osorno; San Pablo; Puyehue; Puerto Octay; Purranque; Río Negro; San Juan de la Costa; Puerto Montt; Puerto Varas; Cochamó; Calbuco; Maullín; Los Muermos; Fresia; Llanquihue; Frutillar; Castro; Ancud; Quemchi; Dalcahue; Curaco de Vélez; Quinchao; Puqueldón; Chonchi; Queilén; Quellón; Chaitén; Hualaihué; Futaleufú; Palena; Coyhaique; Lago Verde; Aysén; Cisnes; Guaitecas; Chile Chico; Río Ibánez; Cochrane; O'Higgins; Tortel; Natales; Torres del Paine; Punta Arenas; Río Verde; Laguna Blanca; San Gregorio; Porvenir; Primavera; Timaukel; Cabo de Hornos; Antártica; Santiago; Independencia; Conchalí; Huechuraba; Recoleta; Providencia; Vitacura; Lo Barnechea; Las Condes; Ñuñoa; La Reina; Macul; Peñalolén; La Florida; San Joaquín; La Granja; La Pintana; San Ramón; San Miguel; La Cisterna; El Bosque; Pedro Aguirre Cerda; Lo Espejo; Estación Central; Cerrillos; Maipú; Quinta Normal; Lo Prado; Pudahuel; Cerro Navia; Renca; Quilicura; Colina; Lampa; Tiltil; Puente Alto; San José de Maipo; Pirque; San Bernardo; Buin; Paine; Calera de Tango; Melipilla; María Pinto; Curacaví; Alhué; San Pedro; Talagante; Peñaflor; Isla de Maipo; El Monte; Padre Hurtado | Personalizado |
| Ejecutivo Junior | `Ejecutivo_Junior` | picklist |  | -; Rommy Leiva; Ricardo Perez; Cristobal Zapata; Estephany Garay; Diego Vargas; Fernando Iturriaga; Mauricio Díaz Méndez; Andres Bilbao; Marcos Arias; Martin Franz; Rodrigo Quintana; Francisco Saavedra; Maximiliano Stein; Mauricio Rojas; Felipe Carrasco; Rodrigo Ubilla; Camila Jofre; David Gomez; Gonzalo Muñoz; Constanza Meza; NO ASIGNADO; Alexander Chapanoff; Andrea Garrido; Camila Donoso; Camila Flores; Daniela Guzman; Darlyn Herrera; Diego Larraín Tapia; Fabiola Zegers; Felipe Norese; Franklin Patricio; Helmut Lammel; Javiera Valderrama; Johnny Felipe Hernandez; Jonathan Jara; Lucas Acuña; Marcelo Hernandez [Marcelo Henandez]; Maximiliano Garafulic; Montserrat Riquelme; Nikolete Jakubonyte; Pablo Velastin; Smiliak Zapata; Valentina Alcaino | Personalizado |
| Fase FinanciaK | `Fase_FinanciaK` | picklist |  | Fase 1; Fase 2; Fase 3; Fase 4; Concluido; Caído | Personalizado |
| IBs | `IBs` | picklist |  | Patricio Gatica; Héctor Venegas; Patricio Olmos; Inversiones Monte Blanco SpA (Máximo Tapia); Vicente Santander; Gustavo Cruzat; Felipe Millar; Hector Venegas; Arturo Sauma; Adolfo Delgado; Raúl Vidal; Jorge Garrido; Dannette Ordoñez; Aldo Antonucci; Juan Gabriel Navarro; Christian Tampe; Patricio Nannig; Scarlette Pacheco | Personalizado |
| Producto | `Producto` | picklist |  | -; Trading; Mutuo; AFI; Leaseback; Departamento; Financiamiento; Venta Propiedad; IB | Personalizado |
| Producto 2 | `Producto_2` | picklist |  | Trading; Mutuo; AFI; Leaseback; Departamento; Financiamiento; IB; Venta Propiedad | Personalizado |
| Social Lead ID | `leadchain0__Social_Lead_ID` | text |  |  | Personalizado |
| Calificación FK | `Rating` | picklist |  | Interesado en Financiamiento [Acquired]; Diferido en Financiamiento [Active]; Archivado en Financiamiento [Market Failed]; No Ubicable en Financiamiento [Project Cancelled]; No Califica en Financiamiento [ShutDown]; No Interesado en Financiamiento |  |
| Calle | `Street` | text |  |  |  |
| Cambiar hora de registro | `Change_Log_Time__s` | datetime |  |  | No escribible vía API |
| Cantidad de empleados | `No_of_Employees` | integer |  |  |  |
| Ciudad | `City` | text |  |  |  |
| Contacto convertido | `Converted_Contact` | lookup |  |  | Lookup → Contacts; No escribible vía API |
| Correo electrónico | `Email` | email |  |  |  |
| Correo electrónico secundario | `Secondary_Email` | email |  |  |  |
| Cuenta convertida | `Converted_Account` | lookup |  |  | Lookup → Accounts; No escribible vía API |
| Código postal | `Zip_Code` | text |  |  |  |
| Descripción | `Description` | textarea |  |  |  |
| Drive | `Website` | website |  |  |  |
| Estado de Posible cliente | `Lead_Status` | picklist |  | Intento de contacto [Attempted to Contact]; Contactar en el futuro [Contact in Future]; Contactado [Contacted]; Posible cliente no solicitado [Junk Lead]; Posible cliente perdido [Lost Lead]; No contactado [Not Contacted]; Previamente clasificado [Pre-Qualified]; No habilitado [Not Qualified] |  |
| Estado de enriquecimiento de datos | `Enrich_Status__s` | picklist |  | Disponible [Available]; Enriched; Data not found | No escribible vía API |
| Estado/Provincia | `State` | text |  |  |  |
| Fecha y hora convertida | `Converted_Date_Time` | datetime |  |  | No escribible vía API |
| Fuente de Posible cliente | `Lead_Source` | picklist |  | Aviso [Advertisement]; Llamada no solicitada [Cold Call]; Recomendación de empleado [Employee Referral]; Recomendación externa [External Referral]; Tienda en línea [OnlineStore]; X (Twitter) [Twitter]; Facebook; Socio [Partner]; Relaciones públicas [Public Relations]; Alias del correo electrónico de ventas [Sales Mail Alias]; Socio de seminarios [Seminar Partner]; Seminario interno [Seminar-Internal]; Exposición comercial [Trade Show]; Descargar web [Web Download]; Investigación web [Web Research]; Chat; Online Store |  |
| Hora de cancelación de suscripción | `Unsubscribed_Time` | datetime |  |  | No escribible vía API |
| Hora de último enriquecimiento de datos | `Last_Enriched_Time__s` | datetime |  |  | No escribible vía API |
| Imagen de Posible cliente | `Record_Image` | profileimage |  |  |  |
| Ingresos anuales | `Annual_Revenue` | currency |  |  |  |
| Modalidad de cancelación de suscripción | `Unsubscribed_Mode` | picklist |  | Formulario de consentimiento [Consent form]; Manual; Enlace de cancelación de suscripción [Unsubscribe link]; Zoho Campaigns [Zoho campaigns] | No escribible vía API |
| Moneda | `Currency` | picklist |  | CLP; USD |  |
| Móvil | `Mobile` | phone |  |  |  |
| No participación del correo electrónico | `Email_Opt_Out` | boolean |  |  |  |
| Nombre completo | `Full_Name` | text |  |  | No escribible vía API |
| País | `Country` | text |  |  |  |
| Propietario de Posible Cliente | `Owner` | ownerlookup |  |  |  |
| Sub IB´s | `Industry` | picklist |  | Mauricio Bucarey; ASP (Proveedor de servicios de aplicaciones) [ASP (Application Service Provider)]; Empresa grande [Large Enterprise]; Empresa pequeña/mediana [Small/Medium Enterprise]; Equipo de almacenamiento [Storage Equipment]; Equipos de redes empresa [Network Equipment (Enterprise)]; ERP; ERP (Planificación de recursos de empresa) [ERP (Enterprise Resource Planning)]; Gestión de redes ópticas [Optical Networking]; Gobierno/Ejército [Government/Military]; Integrador de sistemas [Systems Integrator]; ISV de gestión [ManagementISV]; ISV de no gestión [Non-management ISV]; Management ISV; MSP (proveedor de servicios de gestión) [MSP (Management Service Provider)]; OEM de datos/telecom. [Data/Telecom OEM]; Proveedor de servicios [Service Provider]; Proveedor de servicios de almacenamiento [Storage Service Provider]; Sector de servicios inalámbricos [Wireless Industry] |  |
| Teléfono | `Phone` | phone |  |  |  |
| Tiempo de conversión de Posible cliente | `Lead_Conversion_Time` | integer |  |  | No escribible vía API |
| Transacción convertida | `Converted_Deal` | lookup |  |  | Lookup → Deals; No escribible vía API |
| se ha convertido | `Converted__s` | boolean |  |  | No escribible vía API |

## Contacts

Layouts: Standard (`6839037000000091033`, active)

| Campo visible | API name | Tipo | Oblig. | Valores permitidos | Observaciones |
|---|---|---|---|---|---|
| Atributo IB | `Atributo_IB` | picklist | L | Correo 1; Reunión Jefe de Negocios; Correo 2; Contratos Firmados; Capacitación General [Capacitación Rodrigo]; Correo 3; Capacitación Trading; IB Renta Variable; Sub IB Renta Variable; IB Renta Fija; Sub IB Renta Fija; IB Estratégico [IB Estrategico]; Sub IB Estratégico; Otros Negocios; IB Inactivo; Descartado [Interesado]; Archivado; Capacitación Camilo; En Proceso; Firmado Contrato; Inseguro; No Califica; No Interesado | Obligatorio por layout; Personalizado |
| Producto | `Producto` | picklist | L | -; Trading; Mutuo; AFI; Leaseback; Departamento; Financiamiento | Obligatorio por layout; Personalizado |
| Móvil | `Mobile` | phone | L |  | Obligatorio por layout |
| Nombre Completo | `Last_Name` | text | S |  | Obligatorio de sistema |
| Analista de Inversiones | `Analista_de_Inversiones` | picklist |  | Lucas Justiniano; Diego Vargas; Jose Quevedo; Camilo Bravo; Hari Saits; Marcelo Henandez; Ricardo Perez; Camila Jofre; David Gomez | Personalizado |
| Atributo Broker FK | `Atributo_Broker_FK` | picklist |  | Reunión Inducción; Contrato Enviados; IB - Activado; IB - Inactivo [Eliminado]; No Califica; Negocios Fase 1; Primer Negocio Cerrado; Primer Negocio Enviado | Personalizado |
| Contrato IB | `Contrato_IB` | website |  |  | Personalizado |
| Ejecutivo Junior | `Ejecutivo_Junior` | picklist |  | Marcelo Henandez; Jonathan Jara; Helmut Lammel; Johnny Felipe Hernandez; Felipe Norese; Rommy Leiva; Ricardo Perez; Cristobal Zapata; Camila Donoso; Pablo Velastin; Estephany Garay; Montserrat Riquelme; Darlyn Herrera; Lucas Acuña; Alexander Chapanoff; Nikolete Jakubonyte; Fernando Iturriaga; Valentina Alcaino; Fabiola Zegers; Andres Bilbao; Camila Flores; Franklin Patricio; Marcos Arias; Martin Franz; Francisco Saavedra; Javiera Valderrama; Smiliak Zapata; Maximiliano Stein; Camila Jofre; David Gomez; Mauricio Rojas; Felipe Carrasco; Rodrigo Ubilla; Daniela Guzman | Personalizado |
| RUT | `RUT` | text |  |  | Personalizado |
| Región Broker | `Ciudad_Comuna` | multiselectpicklist |  | Región de Arica y Parinacota [Arica]; Camarones; Región de Tarapacá; Putre; Región de Antofagasta; General Lagos; Región de Atacama; Iquique; Región de Coquimbo; Alto Hospicio; Región de Valparaíso; Pozo Almonte; Región Metropolitana de Santiago; Camiña; Región del Libertador General Bernardo O'Higgins; Colchane; Región del Maule; Huara; Región de Ñuble; Pica; Región del Biobío; Antofagasta; Región de La Araucanía; Mejillones; Región de Los Ríos; Región de Los Lagos; Sierra Gorda; Región de Aysén del General Carlos Ibáñez del Campo; Taltal; Calama; Región de Magallanes y de la Antártica Chilena; Ollagüe; San Pedro de Atacama; Tocopilla; María Elena; Copiapó; Caldera; Tierra Amarilla; Chañaral; Diego de Almagro; Vallenar; Alto del Carmen; Freirina; Huasco; La Serena; Coquimbo; Andacollo; La Higuera; Paihuano; Vicuña; Illapel; Canela; Los Vilos; Salamanca; Ovalle; Combarbalá; Monte Patria; Punitaqui; Río Hurtado; Valparaíso; Casablanca; Concón; Juan Fernández; Puchuncaví; Quintero; Viña del Mar; Isla de Pascua; Los Andes; Calle Larga; Rinconada; San Esteban; La Ligua; Cabildo; Papudo; Petorca; Zapallar; Quillota; La Calera; Hijuelas; La Cruz; Nogales; San Antonio; Algarrobo; Cartagena; El Quisco; El Tabo; Santo Domingo; San Felipe; Catemu; Llay-Llay; Panquehue; Putaendo; Santa María; Quilpué; Limache; Olmué; Villa Alemana; Rancagua; Codegua; Coinco; Coltauco; Doñihue; Graneros; Las Cabras; Machalí; Malloa; Mostazal; Olivar; Peumo; Pichidegua; Quinta de Tilcoco; Rengo; Requínoa; San Vicente; Pichilemu; La Estrella; Litueche; Marchigüe; Navidad; Paredones; San Fernando; Chépica; Chimbarongo; Lolol; Nancagua; Palmilla; Peralillo; Placilla; Pumanque; Santa Cruz; Talca; Constitución; Curepto; Empedrado; Maule; Pelarco; Pencahue; Río Claro; San Clemente; San Rafael; Cauquenes; Chanco; Pelluhue; Curicó; Hualañé; Licantén; Molina; Rauco; Romeral; Sagrada Familia; Teno; Vichuquén; Linares; Colbún; Longaví; Parral; Retiro; San Javier; Villa Alegre; Yerbas Buenas; Chillán; Bulnes; Chillán Viejo; El Carmen; Pemuco; Pinto; Quillón; San Ignacio; Yungay; Quirihue; Cobquecura; Coelemu; Ninhue; Portezuelo; Ránquil; Treguaco; San Carlos; Coihueco; Ñiquén; San Fabián; San Nicolás; Concepción; Coronel; Chiguayante; Florida; Hualqui; Lota; Penco; San Pedro de La Paz; Santa Juana; Talcahuano; Tomé; Hualpén; Lebu; Arauco; Cañete; Contulmo; Curanilahue; Los Álamos; Tirúa; Los Ángeles; Antuco; Cabrero; Laja; Mulchén; Nacimiento; Negrete; Quilaco; Quilleco; San Rosendo; Santa Bárbara; Tucapel; Yumbel; Alto Biobío; Temuco; Carahue; Cunco; Curarrehue; Freire; Galvarino; Gorbea; Lautaro; Loncoche; Melipeuco; Nueva Imperial; Padre Las Casas; Perquenco; Pitrufquén; Pucón; Saavedra; Teodoro Schmidt; Toltén; Vilcún; Villarrica; Cholchol; Angol; Collipulli; Curacautín; Ercilla; Lonquimay; Los Sauces; Lumaco; Purén; Renaico; Traiguén; Victoria; Valdivia; Corral; Lanco; Los Lagos; Máfil; Mariquina; Paillaco; Panguipulli; La Unión; Futrono; Lago Ranco; Río Bueno; Puerto Montt; Calbuco; Cochamó; Fresia; Frutillar; Los Muermos; Llanquihue; Maullín; Puerto Varas; Castro; Ancud; Chonchi; Curaco de Vélez; Dalcahue; Puqueldón; Queilén; Quellón; Quemchi; Quinchao; Osorno; Puerto Octay; Purranque; Puyehue; Río Negro; San Juan de la Costa; San Pablo; Chaitén; Futaleufú; Hualaihué; Palena; Coyhaique; Lago Verde; Aysén; Cisnes; Guaitecas; Cochrane; O'Higgins; Tortel; Chile Chico; Río Ibáñez; Punta Arenas; Laguna Blanca; Río Verde; San Gregorio; Cabo de Hornos; Antártica; Porvenir; Primavera; Timaukel; Natales; Torres del Paine; Santiago; Cerrillos; Cerro Navia; Conchalí; El Bosque; Estación Central; Huechuraba; Independencia; La Cisterna; La Florida; La Granja; La Pintana; La Reina; Las Condes; Lo Barnechea; Lo Espejo; Lo Prado; Macul; Maipú; Ñuñoa; Pedro Aguirre Cerda; Peñalolén; Providencia; Pudahuel; Quilicura; Quinta Normal; Recoleta; Renca; San Joaquín; San Miguel; San Ramón; Vitacura; Puente Alto; Pirque; San José de Maipo; Colina; Lampa; Til Til; San Bernardo; Buin; Calera de Tango; Paine; Melipilla; Alhué; Curacaví; María Pinto; San Pedro; Talagante; El Monte; Isla de Maipo; Padre Hurtado; Peñaflor | Personalizado |
| Social Lead ID | `leadchain0__Social_Lead_ID` | text |  |  | Personalizado |
| Venta Inmobiliaria | `Venta_Inmobiliaria` | picklist |  | En Proceso (Contrato Firmado con Cliente); Publicado en Wasi; En Negociación; Tomado Por Inversionista; Estudio Títulos (Proceso Bancario); Vendido | Personalizado |
| Asistente | `Assistant` | text |  |  |  |
| Cambiar hora de registro | `Change_Log_Time__s` | datetime |  |  | No escribible vía API |
| Ciudad para correspondencia | `Mailing_City` | text |  |  |  |
| Correo electrónico | `Email` | email |  |  | Único |
| Correo electrónico corporativo | `Secondary_Email` | email |  |  |  |
| Corresponde Pago | `Skype_ID` | text |  |  |  |
| Código postal para correspondencia | `Mailing_Zip` | text |  |  |  |
| Departamento | `Department` | text |  |  |  |
| Descripción | `Description` | textarea |  |  |  |
| Domicilio para correspondencia | `Mailing_Street` | text |  |  |  |
| Estado de enriquecimiento de datos | `Enrich_Status__s` | picklist |  | Disponible [Available]; Enriched; Data not found | No escribible vía API |
| Estado para correspondencia | `Mailing_State` | text |  |  |  |
| Fuente de Posible cliente | `Lead_Source` | picklist |  | Aviso [Advertisement]; Llamada no solicitada [Cold Call]; Recomendación de empleado [Employee Referral]; Recomendación externa [External Referral]; Tienda en línea [OnlineStore]; Socio [Partner]; X (Twitter) [Twitter]; Facebook; Relaciones públicas [Public Relations]; Alias del correo electrónico de ventas [Sales Mail Alias]; Socio de seminarios [Seminar Partner]; Seminario interno [Seminar-Internal]; Exposición comercial [Trade Show]; Descargar web [Web Download]; Investigación web [Web Research]; Casos de la Web [Web Cases]; Correo web [Web Mail]; Chat; Online Store |  |
| Hora de cancelación de suscripción | `Unsubscribed_Time` | datetime |  |  | No escribible vía API |
| Hora de último enriquecimiento de datos | `Last_Enriched_Time__s` | datetime |  |  | No escribible vía API |
| Imagen de Contacto | `Record_Image` | profileimage |  |  |  |
| Modalidad de cancelación de suscripción | `Unsubscribed_Mode` | picklist |  | Formulario de consentimiento [Consent form]; Manual; Enlace de cancelación de suscripción [Unsubscribe link]; Zoho Campaigns [Zoho campaigns] | No escribible vía API |
| N.º de teléfono del asistente | `Asst_Phone` | phone |  |  |  |
| Nombre completo | `Full_Name` | text |  |  | No escribible vía API |
| Nombre de Cuenta | `Account_Name` | lookup |  |  | Lookup → Accounts |
| Otra ciudad | `Other_City` | text |  |  |  |
| Otro código postal | `Other_Zip` | text |  |  |  |
| Otro domicilio | `Other_Street` | text |  |  |  |
| Otro estado | `Other_State` | text |  |  |  |
| Otro país | `Other_Country` | text |  |  |  |
| País para correspondencia | `Mailing_Country` | text |  |  |  |
| Propietario de Contacto | `Owner` | ownerlookup |  |  |  |
| Teléfono | `Phone` | phone |  |  |  |

## Accounts

Layouts: Standard (`6839037000000091029`, active)

| Campo visible | API name | Tipo | Oblig. | Valores permitidos | Observaciones |
|---|---|---|---|---|---|
| Analista de Inversiones | `Analista_de_Inversiones` | picklist | L | Diego Vargas; Hari Saits; Marcelo Henandez; Pendiente; Ricardo Perez; David Gomez; Camila Jofre; Camilo Bravo; Jose Quevedo; Lucas Justiniano | Obligatorio por layout; Personalizado |
| Ejecutivo Junior | `Ejecutivo_Junior` | picklist | L | -; Marcelo Henandez; Johnny Felipe Hernandez; Felipe Norese; Rommy Leiva; Ricardo Perez; Estephany Garay; Alexander Chapanoff; Fernando Iturriaga; Valentina Alcaino; Fabiola Zegers; Andres Bilbao; Martin Franz; Franklin Patricio; Camila Flores; Marcos Arias; Rodrigo Quintana; Francisco Saavedra; Javiera Valderrama; Smiliak Zapata; Maximiliano Stein; Mauricio Rojas; Felipe Carrasco; Rodrigo Ubilla; Andrea Garrido; Camila Donoso; Cristobal Zapata; Daniela Guzman; Darlyn Herrera; Helmut Lammel; Jonathan Jara; Lucas Acuña; Maximiliano Garafulic; Montserrat Riquelme; Nikolete Jakubonyte; Pablo Velastin | Obligatorio por layout; Personalizado |
| Etapa del Cliente | `IBs_Atributo` | picklist | L | Deposito Recibido; Contratos Firmados [Archivado]; Credenciales Enviadas + Forms; Reversado a Ejecutivo; Validación Compliance; Habilitación de Cuenta; Traspaso a Post Venta; Avanzado; Inseguro; Referido | Obligatorio por layout; Personalizado |
| Producto | `Producto` | picklist | L | Trading; Mutuo; AFI; Leaseback; Departamento; Financiamiento; IB | Obligatorio por layout; Personalizado |
| RUT Cliente | `RUT` | text | L |  | Obligatorio por layout; Personalizado |
| Calificación | `Rating` | picklist | L | En Proceso; Caído; Cliente Activo (operando contínuamente) [Acquired]; Cliente Inactivo (con dinero para operar) [Active]; Cliente Quemado y Retirado (Perdío parte de su capital y retiró) [Market Failed]; Cliente con Ganancias y retirado (Gano capital y se retiró) [Project Cancelled]; Cliente Quemado (Perdío casi o todosucapital) [ShutDown]; Reactivado; Referido | Obligatorio por layout |
| Modalidad de Operación | `Account_Type` | picklist | L | Manual [Supplier]; MAM; BOT; Otro Producto Activo; Inactiva [Vendor]; Analista [Analyst]; Cliente [Customer]; Competidor [Competitor]; Distribuidor [Distributor]; Integrador [Integrator]; Inversor [Investor]; Otro [Other]; Posible [Prospect]; Prensa [Press]; Revendedor [Reseller]; Socio [Partner] | Obligatorio por layout |
| Móvil | `Phone` | phone | L |  | Obligatorio por layout |
| Nombre de Cuenta | `Account_Name` | text | S |  | Obligatorio de sistema |
| Contrato AFI | `Contrato_Afi` | website |  |  | Personalizado |
| Contrato GI | `Contrato_Cfd` | website |  |  | Personalizado |
| Contrato Mutuo | `Contrato_Mutuo` | website |  |  | Personalizado |
| Correo Contacto | `Correo_Contacto` | email |  |  | Personalizado |
| IB Principal | `IBs` | picklist |  | No Corresponde; Patricio Gatica; Héctor Venegas; Patricio Olmos; Inversiones Monte Blanco SpA (Máximo Tapia); Vicente Santander; Gustavo Cruzat; Arturo Sauma; Felipe Millar; Adolfo Delgado; Raúl Vidal; Jorge Garrido; Juan Gabriel Navarro; Dannette Ordoñez; Christian Tampe; Patricio Nannig; Scarlette Pacheco | Personalizado |
| Broker FK | `Ownership` | picklist |  | Abel Cancino Asesor [Private]; Alejandra Madrid Martinez Asesor; Alejandro Vielma Asesor; Alexis Garrido Asesor; Alexis Muñoz Medina Asesor; Andres Alejandro Bilbao Pozo; Angelica Medina Asesora; Angelina Zuñiga Asesora; Bernardita Pizarrón Asesora; Carlos Godoy Guajardo Asesor; Carlos Javier Barria; Carlos Olguin; Carolina Nallar; Carolina Soto; Christian Tampe Asesor; Christopher Díaz Suarez Asesor; Claudia Saldaña Asesora; Cristian Fonseca Asesor; Daniel Heinrich Asesor; Dannette Ordoñez Henriquez; David Ocaranza Asesor; Esteban Retamal Santibañez; Fabian Valenzuela Asesor; Gabriela Soto Asesora; Godfrey Dawson; Gonzalo Moyano Asesor Comercial; Gonzalo Risso Asesores; Jaime Sandoval Asesor; Javier Bunster; Javiera Perez Valdes Asesor; Jesus Cruces Palma; Jorge Castillo; Jorge Yanez Mardonez Asesor; José Luis Cifuentes Martinez Asesor M; José Luis Jiménez Orellana Asesor; Jose Luis Muñoz Asesor; José Padilla Asesor; Jose Saez; Juan Elgueta Asesor; Juan Enrique Urquhart Asesor; Karen Inostroza Asesora; Kenita Moya Asesora; León Vidal Asesor; Leonardo Medina M&M Asesor; Lionel Rubio Aceituno; Luckas Ortiz; Luis Cabrera Retamal Asesor; Luis Correa Asesor; Luis Hidalgo Asesor; Manuel González Asesor; Marcelo James Harmitton; Marcelo Mocelli Asesor; Marco Antonio Ureta Asesor; Marco Cornejo Asesor; Marcos Ponce Asesor; Maria Angelica Pérez Gallardo Asesora; Maria Susana Salazar Jara Asesora Financiak; Mauricio Arancibia Rojas Asesor; Mauricio Coloma Asesor; Mauricio Pérez Celedon Asesor; Mauro Escobar Salgado; Oliver Diaz; Pablo Castro Asesor; Pablo Mercado Asesor; Pablo Solís J.; Paola Rodríguez Fuentes Asesora; Paola Rojas Asesora; Patricio Caceres Asesor Pinilla; Patricio Herrera Asesor; Patricio Nuñez Asesor; Paulina Ninoska Nuñez Asesora; Renato Eugenio Ezquerro carrillo Asesor; Richard Morales Asesor; Rita Solange Castro Gonzalez Asesor; Roberto Fuentes Ramirez Asesor; Roberto González Caceres Asesor; Rodrigo Garrido Alvear Asesor; Rosa Irene Basualto Yañez; Sandra Dueñas Riffo Asesora; Sebastián de Rementería Asesor; Sebastian Valenzuela Gil; Sergio Arcos Illanes Asesor; Victor Perez Cid Asesor; Virginia Contreras; Firmado [Public Company]; Government; Inhabilitado [Other]; Partnership; Privately Held; Público [Public]; Subsidiario [Subsidiary] |  |
| Cambiar hora de registro | `Change_Log_Time__s` | datetime |  |  | No escribible vía API |
| Ciudad de envío | `Shipping_City` | text |  |  |  |
| Ciudad de facturación | `Billing_City` | text |  |  |  |
| Cuenta principal | `Parent_Account` | lookup |  |  | Lookup → Accounts |
| Código de envío | `Shipping_Code` | text |  |  |  |
| Código de facturación | `Billing_Code` | text |  |  |  |
| Descripción | `Description` | textarea |  |  |  |
| Domicilio de envío | `Shipping_Street` | text |  |  |  |
| Domicilio de facturación | `Billing_Street` | text |  |  |  |
| Estado de enriquecimiento de datos | `Enrich_Status__s` | picklist |  | Disponible [Available]; Enriched; Data not found | No escribible vía API |
| Estado de envío | `Shipping_State` | text |  |  |  |
| Estado de facturación | `Billing_State` | text |  |  |  |
| Hora de último enriquecimiento de datos | `Last_Enriched_Time__s` | datetime |  |  | No escribible vía API |
| Imagen de Cuenta | `Record_Image` | profileimage |  |  |  |
| Link Formulario de Trading | `Website` | website |  |  |  |
| N° Cuenta MT5 | `Account_Number` | bigint |  |  |  |
| País de envío | `Shipping_Country` | text |  |  |  |
| País de facturación | `Billing_Country` | text |  |  |  |
| Propietario de Cuenta | `Owner` | ownerlookup |  |  |  |
| Sub IB | `Industry` | picklist |  | Mauricio Bucarey [ASP (Application Service Provider)]; Communications; Consulting; Education; Empresa grande [Large Enterprise]; Empresa pequeña/mediana [Small/Medium Enterprise]; Equipo de almacenamiento [Storage Equipment]; Equipos de redes empresa [Network Equipment (Enterprise)]; ERP (Planificación de recursos de empresa) [ERP (Enterprise Resource Planning)]; Financial Services; Gestión de redes ópticas [Optical Networking]; Gobierno/Ejército [Government/Military]; Integrador de sistemas [Systems Integrator]; ISV de gestión [ManagementISV]; ISV de no gestión [Non-management ISV]; Manufacturing; MSP (proveedor de servicios de gestión) [MSP (Management Service Provider)]; OEM de datos/telecom. [Data/Telecom OEM]; Proveedor de servicios [Service Provider]; Proveedor de servicios de almacenamiento [Storage Service Provider]; Real Estate; Sector de servicios inalámbricos [Wireless Industry]; Technology |  |

## Deals

Layouts: Standard (`6839037000000091023`, active)

| Campo visible | API name | Tipo | Oblig. | Valores permitidos | Observaciones |
|---|---|---|---|---|---|
| Analista de Inversiones | `Analista_de_Inversiones` | picklist | L | Lucas Justiniano; Camilo Bravo; Diego Vargas; Jose Quevedo; Hari Saits; Marcelo Henandez; Ricardo Perez; Camila Jofre; David Gomez | Obligatorio por layout; Personalizado |
| Producto | `Producto` | picklist | L | Trading; Mutuo; AFI; Leaseback; Departamento; Financiamiento | Obligatorio por layout; Personalizado |
| Fase | `Stage` | picklist | S | Clasificación [Qualification]; Necesita análisis [Needs Analysis]; Propuesta de valor [Value Proposition]; Identificar responsables [Id. Decision Makers]; Cotización de propuesta/precio [Proposal/Price Quote]; Negociación/revisión [Negotiation/Review]; Cerrado ganado [Closed Won]; Cerrado perdido [Closed Lost]; Perdido y cerrado para la competencia [Closed Lost to Competition]; Identify Decision Makers | Obligatorio de sistema |
| Fecha de cierre | `Closing_Date` | date | L |  | Obligatorio por layout |
| Nombre de Cuenta | `Account_Name` | lookup | L |  | Obligatorio por layout; Lookup → Accounts |
| Nombre de Trato | `Deal_Name` | text | S |  | Obligatorio de sistema |
| Tipo | `Type` | picklist | L | Negocios existentes [Existing Business]; Nuevo negocio [New Business] | Obligatorio por layout |
| Administrador Externo | `Administrador_Externo` | picklist |  | Camilo Bravo | Personalizado |
| Comprobante Deposito / Transferencia | `Comprobante_Deposito_Transferencia` | fileupload |  |  | Personalizado; Tooltip: Se cargas el comprobante de deposito, transferencia, vale vista o instrumento que uso para la carga de su capital |
| Comprobante Rescate | `Comprobante_Rescate` | fileupload |  |  | Personalizado |
| Deal | `Deal` | integer |  |  | Personalizado |
| Ejecutivo Junior | `Ejecutivo_Junior` | picklist |  | Marcelo Henandez; Jonathan Jara; Helmut Lammel; Johnny Felipe Hernandez; Felipe Norese; Rommy Leiva; Ricardo Perez; Cristobal Zapata; Camila Donoso; Pablo Velastin; Estephany Garay; Montserrat Riquelme; Darlyn Herrera; Alexander Chapanoff; Lucas Acuña; Nikolete Jakubonyte; Fernando Iturriaga; Valentina Alcaino; Fabiola Zegers; Andres Bilbao; Andrea Garrido; Daniela Guzman; Maximiliano Garafulic | Personalizado |
| IBs | `IBs` | picklist |  | Patricio Gatica; Patricio Olmos; Inversiones Monte Blanco SpA (Máximo Tapia); Vicente Santander; Arturo Sauma; Adolfo Delgado; Gustavo Cruzat; Hector Venegas; Felipe Millar; Raúl Vidal; Jorge Garrido; Christian Tampe | Personalizado |
| Social Lead ID | `leadchain0__Social_Lead_ID` | text |  |  | Personalizado |
| Sub IB´s | `Sub_IB_s` | picklist |  | Mauricio Bucarey | Personalizado |
| Cambiar hora de registro | `Change_Log_Time__s` | datetime |  |  | No escribible vía API |
| Descripción | `Description` | textarea |  |  |  |
| Duración del ciclo de ventas | `Sales_Cycle_Duration` | integer |  |  | No escribible vía API |
| Duración total de las ventas | `Overall_Sales_Duration` | integer |  |  | No escribible vía API |
| Fuente de Campaña | `Campaign_Source` | lookup |  |  | Lookup → Campaigns |
| Fuente de Posible cliente | `Lead_Source` | picklist |  | Aviso [Advertisement]; Llamada no solicitada [Cold Call]; Recomendación de empleado [Employee Referral]; Recomendación externa [External Referral]; Tienda en línea [OnlineStore]; Socio [Partner]; Relaciones públicas [Public Relations]; Alias del correo electrónico de ventas [Sales Mail Alias]; Socio de seminarios [Seminar Partner]; Seminario interno [Seminar-Internal]; Exposición comercial [Trade Show]; Descargar web [Web Download]; Investigación web [Web Research]; Chat |  |
| Hora de modificación de fase | `Stage_Modified_Time` | datetime |  |  |  |
| Importe | `Amount` | currency |  |  |  |
| Ingresos esperados | `Expected_Revenue` | currency |  |  |  |
| Moneda | `Currency` | picklist |  | CLP; USD |  |
| Motivo de la pérdida | `Reason_For_Loss__s` | picklist |  | Discrepancia de expectativa [Expectation Mismatch]; Precio [Price]; Cliente no cualificado [Unqualified Customer]; Falta de respuesta [Lack of response]; Seguimientos perdidos [Missed Follow Ups]; Objetivo incorrecto [Wrong Target]; Competencia [Competition]; Interés futuro [Future Interest]; Otro [Other] |  |
| Nombre de Contacto | `Contact_Name` | lookup |  |  | Lookup → Contacts |
| Probabilidad (%) | `Probability` | integer |  |  |  |
| Propietario de Trato | `Owner` | ownerlookup |  |  |  |
| Siguiente paso | `Next_Step` | text |  |  |  |
| Tiempo de conversión de Posible cliente | `Lead_Conversion_Time` | integer |  |  | No escribible vía API |

Campos de sistema omitidos de las tablas (solo lectura): `Closed_Time`, `Created_By`, `Created_Time`, `Exchange_Rate`, `Last_Activity_Time`, `Locked__s`, `Modified_By`, `Modified_Time`, `Record_Status__s`, `Tag`, `id`
