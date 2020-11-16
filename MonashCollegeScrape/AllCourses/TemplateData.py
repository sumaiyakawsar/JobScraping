level_key = {'VOC': ['Vocational'],
             'DIP': ['Diploma', 'DIP'],
             'ADIP': ['Advanced Diploma'],
             'ADEG': ['Associate Degree'],
             'FUG': ['FD', 'FDs', 'FDEd', 'FdEd', 'FdA', 'FDA', 'FDArts', 'FDEng', 'FdSc', 'A.A.', 'A.S.',
                     'A.A.S', 'A.A.S.'],
             'Found': ['Foundation'],
             'BA': ['Bachelor', 'B.Trad.', 'BGInS', 'BAcc', 'BAFM', 'BAdmin', 'BAS', 'BAA', 'BASc', 'BASc/BEd',
                    'BArchSc', 'BAS', 'BA', 'BAS', 'BASc/BEd', 'BASc', 'BA/BComm', 'BA/BEd', 'BA/BEd/Dip', 'BA/LLB',
                    'BA/MA', 'BBRM', 'BBA', 'BBA/BA', 'BBA/BCS', 'BBA/BEd', 'BBA/BMath', 'BBA/BSc', 'BBE', 'BBTM',
                    'BDS', 'BCogSc', 'BComm', 'BCom', 'BCoMS', 'BCoSc', 'BCS', 'BComp', 'BCmp', 'BCFM', 'BDes', 'BDEM',
                    'BEcon', 'BEng', 'BEng&Mgt', 'BEngSoc', 'BESc', 'BEngTech', 'BEM', 'BESc', 'BESc/BEd', 'BES',
                    'BES/BEd', 'BFAA', 'BFA,BFA/BEd', 'BFS', 'BGBDA', 'BHP', 'BHSc', 'BHSc', 'BHS', 'BHS/BEd',
                    'BHum', 'BHK', 'BHRM', 'BID', 'BINF', 'BIT', 'BID', 'BIB', 'BJ', 'BJour', 'BJourn', 'BJHum',
                    'BKin', 'BK/BEd', 'BKI', 'BLA', 'BMOS', 'BMath', 'BMath/BEd', 'BMPD', 'BMRSc', 'BMSc', 'BMus',
                    'MusBac', 'BMusA', 'BMus/BEd', 'BMuth', 'BOR', 'BOR/BA', 'BOR/BEd', 'BOR/BSc', 'BPHE', 'BPhEd',
                    'BPHE/BEd', 'BPA', 'BPAPM', 'BPH', 'BRLS', 'BSc', 'BSc&Mgt', 'BSc/BASc', 'BSc/BComm', 'BSc/BEd',
                    'BSc(Eng)', 'BScFS', 'BScF', 'BSc(Kin)', 'BScN', 'BSocSc', 'BSW', 'BSE', 'BSM', 'BTech', 'BTh',
                    'BURPI', 'HND', 'HNC', 'iBA,iBA/BEd', 'iBBA', 'iBSc', 'iBSc/BEd', 'LLB', 'MEng', 'MChem',
                    'MPharm', 'MBiol', 'PCE', 'MBChB', 'DipHE', 'AS', 'BS', 'BSN', 'BSME', 'BSB', 'BSCH', 'BSA', 'BSEE',
                    'BLS', 'BSCE', 'BSCMPE', 'B.S.', 'B.A.', 'B.S.F.', 'B.M.', 'Major', 'Cognate', 'NSB', 'B.F.A.',
                    'First', '1st', 'Bachelor\'s', 'B.Sc.'],
             'BAH': ['Bachelor honours'],
             'GDIP': ['Graduate Diploma'],
             'GCERT': ['Graduate Certificate', 'PGCE ', 'PgC'],
             'PG': ['Postgraduate'],
             'MST': ['Master', 'MA', 'M.A.', 'A.M.', 'MPhil', 'M.Phil.', 'MSc', 'M.S.', 'SM', 'MBA', 'M.B.A.', 'MSci',
                     'LLM', 'LL.M.', 'MMath', 'MPhys', 'MPsych', 'MRes' 'MSci', 'LMHC', 'MSEd', 'MS', 'MSE', 'MSECE',
                     'DNP', 'MSME', 'M.Ed.', 'M.Eng.', 'M.C.T.L.', 'M.I.P.', 'M.F.A', 'M.P.A.', 'M.P.P.', 'M.F.A.',
                     'M.A.L.S.', 'M.P.H.', 'M.A.T.', 'M.S.T.', 'M.S.W.', 'M.I.C.L.J.', 'M.S.W.',
                     'License', 'MDes', 'MRes', 'MMus', 'MEval', 'Master\'s', '2nd', 'M.Sc.', 'Pre-master'],
             'DOC': ['Doctor', 'Doctorate', 'ClinPsyD', 'D.D.', 'L.H.D.', 'Litt.D.', 'Ed.S.',
                     'LTD ', 'LL.D.', 'Mus.D.', 'S.D.', 'DPharm', 'Third'],
             'PHD': ['PhD', 'Ph.D.'],
             'Minor': ['Minor'],
             'SHORT COURSES': ['Short', 'Course'],
             'SEMINAR': ['Seminar'],
             'PRODEV': ['Tailor'],
             'CONF': ['Conference'],
             'HONS': ['Honours', 'Hons'],
             'CERTIV': ['Certificate IV'],
             'CERTIII':['Certificate III'],
             'EN':['IELTS','English']
             }

faculty_key = {
    'Art, Design and Architecture': ['architectural design', 'design', 'architectural', 'art', 'architecture'],
    'Art': ['architectural design', 'design', 'architectural', 'art', 'architecture'],
    'Business & Economics': ['accounting','management',' Joinery','Fiscale Economie','imagineering','Fiscale','ibs','open','origini','finanza','essec','mim','lse','cems','organization','NCC','ppe','finance','business','administration','global','arrange','commerce','resource','marketing','supply','financial','services','economics','corporate','sustainability','capital','market','math','spss','economic','proffesional','numer','entrepreneurship','property','banking','analytics','budget','taxation','bank','auditing','control','analysis','basel','statement','modelling','macroeconomic','logistics','advertising','trade','real','statistic','estate','promotion','enterprise','actuarial','strategy','specialist','accountancy','behavioural','econometrics','bus','insurance','margin','regression','reliability','keeping','innovation','vat','macroeconomics','aat','att','cfa','cfq','cisi','cpci','cpi','cppi','cta','fia','icaew','icas','icsa','imc','jieb','investments','money','portfolio','derivatives','foreign','exchange','cima','administrative','events','risk','resource','merger','growing','acquisition','economy','investment','manage','management','organisations','mortgage','conference','manager','commercer','organisation','quality','interdisciplinary','acca','logistic','algebra','strategic','international relation','nonprofit','process','frs','influencing','procurement','strategies','practising','negotiation','negotiating','purchasing','shipping','operations','treasury','investing','asset','actuary','accountant','m.b.a','manufacturing','retailing','commodities','celebrancy','MBA','specific','EnvEuro','branding','advertisement','marxism','zommertse','bba','BBA','consulting','economist','mba','sales','gestion','clerk','erp','supervision','ecommerce'],
    'Education': ['childhood','Human Movement','Geschiedenis','think','education','teaching','numeracy','education',
                  'discipline','educational','schooling','junior','needs','ratep','views','learn','black','writers',
                  'race','years','disable','indigenous','prep','catholic','leading','difficulties','speaking','second',
                  'progressive','evaluation','parent','pgce','coordinator','primary','gifted','work','progress','baccalaureate',
                  'introduction','contexts','birth','five','expert','inclusive','curriculum','principal','preparation','accelerated',
                  'tertiary','senior','philosophies','student','students','academic', 'semiotics','intervention','ducier','managing',
                  'toddler','guidance','teach','visiting','education','salon','coach','integrationist','education','national'],
    'Engineering': ['engineering','M.E.', 'bioengineering','B.E.(Hons.)','bngineer','research','Aircraft','mechanical','metallurgical','renewable','municipal','transportation','extractive','metallurgy','petroleum','civil','electical','Mechanics','motorsport','robotic','microelectronic','mechatronics','infrastructure','instrumentation','mechatronic','geospacial','photovoltaics','solar','aeronautical','structures','electrical','powercraft','decommissioning','utility','subsea','mapping','intrumentation','automation','pollution','bioresource','imeche','biochemical','autonomous','fluids','geomechanical','naval','fire','sciencce','ventilation','photov','innovative','vehicle','oil','gas','efficient','fabrication','specialising','units','mechanical','equipment','graphene','cybernetics','mechanics','machining','lineworker','aerodynamics','electrochemistry','engineer','industrial','mobility','geodesy','medtech','Mechanical','Motosport','automotive','pneumatics','professional','Maschinenbau','Mechatronik','mechanic','forklift','repair','electrician','locksmith','technician','plumber','pipefitter'],
    'Law': ['law','government','bar','tax','victimology','legal','juris','policy','jurisprudence','criminal','justice','criminology','investigation','deviance','prevention','advocacy','commincations','copyright','defamation','rights','intellectual','negotiation','patents','dispute','conveyancing','production','inquiry','intelligence','police','crime','policing','leases','undertaking','contract','pedagogy','ethics','ethical','action','regulation','lba','criminological','regulatory','comparative','juridical','migration','labour','private','corporations','miclaw','parliamentary','rotc','forensic','j.d','commercial','public affairs','diplomacy','arbitration','future','ll.m.','argumentation','magister','legum','Legislative','paralegal'],
    'Medicine, Nursing and Health Sciences': ['biomedicine','herbal','Physiotherapist','hiv','nhet','Bioscience','denturist','opticianry','Rheumatology','Gastroenterology','Cardiology','Nephrology','Endocrinology','oral','physiotherapy','pathology','biomedical','nursing','medical','surgery','accident','sonography','paramedic','prehospital','pharmacy','dental','physiology','podiatric','preclinical','paramedical','activity','diagnostics','pharmaceuticals','evidence','cognitive','mind','anatomy','orthoptics','dementia','prosthetics','orthotics','phatmaceutical','discovery','paramedicine','dependency','haematology','transfusions','transplantation','cytopathology','histopathology','radiations','osteopathy','osteopathic','kinesiology','epidemiology','biomechanics','prescription','injury','motor','pharmacist','instruction','coordination','dentistry','joint','diagnostic','injuries','radiography','preventive','histology','context','neurobiology','traditional','therapeutic','dermal','therapies','preliminary','musculoskeletal','physiotherapy','specialisations','tissue','sexology','critical','protection','diabetes','cancer','periodontology','acute','initial','registration','overseas','nurses','specialised','embryology','minimally','invasive','anaesthetics','recovery','burns','cardiac','gerontological','pharmaceutics','infection','intensive','attachment','oncology','orthopaedic','perioperative','renal','anaesthetic','apheresis','hyperbaric','sleep','odontology','ultrasound','trials','breast','cataract','refractive','restorative','orthodontics','prescribers','paediatric','periodontics','prosthodontics','otolaryngology','m.ost','immunity','pharmacology','inflammation','neurophysiology','stis','sexual','metabolic','cardiothoracic','colorectal','endocrine','head','neck','neurosurgery','otorhinolaryngology','reconstructive','outcomes','transplant','upper','gastrointestinal','urology','vascular','endovascular','complex','careageing','palliation','nurse','practitioner','medicine','obstetrics','gynaecology','philosophypublic','endodontics','infectious','dentistry','clinical','paraclinical','dentistry','medicine','biological','medicine','clinical','medicine','philosophymedicine','testing','ambulance','medication','histotechnician','women','personal support','clinician','prescribing','spinal','allergy','neonatology','anxiety','CBT','surgeon','Podiatrist','Psychologist','Podology','geriatrics','logopedics','Acupuncture','Biomedizintechnik','rongo_','koroua','clinical'],
    'Pharmacy and Pharmaceutical Sciences': ['natural','ecotoxicology','Bioscience','Nanoscience','each','Malting','BEC','ENHET','Reschem','Medical','biological','orthoptic','dietistic','environmental','nanoscience','Physiotheraphy','Linear', "A Levels",'Chemistry', 'Narrative','M.Pharm.','B.Pharm.(Hons.)','M.Sc.(Hons.)','bionanotechnology','Suivi','seagriculture','health','marine','environment','podiatry','nutrition','molecular','nhet','physician','genetics','dietetics','classification','reproductive','microbiology','immunology','nutritional','biochemistry','plant','zoology','botany','ecology','animal','theoretical','water','forest','sustain','chiropractic','analytical','conservation','wildlife','coastal','equine','veterinary','mine','surveying','biological','conservation','addiction','freshwater','evolution','organismal','hydrology','ocean','biodiversity','team','clean','aquatic','ecosystems','gcp','ich','regional','indigenous','cradle','grave','population','coasts','astronomy','assyriology','catchments','geomorphology','terrestrial','outdoor','atmospheric','developmental','drug','formulation','resonance','geotechnical','meteorolgy','pharmaceutical','chemical','psychiatry','statistical','proteomics','anthropometry','physic','structure','leisure','function','geology','geomatic','chemistry','kinetics','pedorthic','foot','care','ecochemistry','evolutionary','laser','space','soil','sport','experimental','disease','cell','weather','canine','fossil','climate','energy','fuels','deposits','audiometry','physiological','material','plants','oceanography','vision','life','agronomy','neuro','archaeological','biophysics','geological','stata','geospatial','measurement','statics','metabolism','monitoring','fisheries','nautical','antarctic','wilderness','wellbeing','nuclear','ear','rehabilitation','geostatistics','parasitology','outreach','medicine','biology','functional','assessment','autism','spectrum','disorders','psychotherapy','gerontology','audiology','loss','grief','trauma','palliative','developing','strength','service','suicide','suicidology','disaster','refugee','tropical','hygiene','retrieval','bhet','biosecurity','preparedness','communicable','protected','area','minerals','ageing','aged','dietetic','ohs','ergonomics','promoting','spiritual','radiopharmaceutical','midwifery','bioethics','chronic','occupational','lifestyle','entomology','factors','hiv','pharmacotherapy','therapy','biotech','geoinformatics','transport','adaptation','biostatistics','bramind','genetic','disability','ophthalmology','ophthalmic','qualitative','microscopy','microanalysis','statistical modelling','extension maths','health','biochem','optometry','radiation','reconstruction','paediatrics','surgical','gender','professions','dissertation','anatomical','neuropsychology','hydrogeology','surveillance','packaging','emergency','diseases','food','alcohol','drugs','myotherapy','fitness','psychology','bioinformatics','chemical','chemistry','astrophysics','biology','physic','sci','cardiovascular','meteorology','biosciences','bioscience','micropalaeontology','toxicology','tomography','polymer','microtechnology','nanostructures','chemist','stomatology','NGENTU','logopedia','archeology','mental','geosciences','recycling','pediatric','hydrography','gynaecological','Physiotherapie','wound','biogeosciences','H\x9arakustik','Philosophie','Geophysics','Paleontology','reflexology',
    'kettlebells','circuit','yoga','sen','trainer','behavioural','psycho'],
    'Science': ['science','bioscience'],
    'Information Technology': ['information', 'industry', '.NET', 'Impit', 'ai', 'M.Sc.(Tech.)', 'routing', 'autodesk',
                               'adobe', 'mining', 'Thesis', 'algorithmic', 'procedural', 'programming', 'technology',
                               'digital', 'data', 'web', 'i.t.', 'security', 'computational', 'computer',
                               'microprocessors', 'intelligent', 'mechatronic', 'photonic', 'games', 'networking',
                               'internet', 'cybersecurity', 'entertainment', 'nanotechnology', 'network', 'graphics',
                               'interactivity', 'software', 'mobile', 'computing', 'application', 'mainframe',
                               'robotics', 'applications', 'cloud', 'infor', 'mation', 'networked', 'system', 'game',
                               'interface', 'scientific', 'remote', 'sensing', 'archives', 'recordkeeping', 'wireless',
                               'internetworking', 'informatics', 'records', 'bioinformatics', 'website', 'technical',
                               'cad', 'artificial', 'myob', 'integrated', 'technology', 'integrated', 'IoT',
                               'interactive', 'technologies', 'eletronics minor', 'Electronics', 'IT',
                               'applied computer science', 'ITT', 'it', 'cisco', 'Cyberfraude', 'Cyberfraude'],

    }