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
             'UG': ['Undergraduate'],
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
             'SHORT COURSES': ['Short', 'Course'], 'SEMINAR': ['Seminar'], 'PRODEV': ['Tailor'], 'CONF': ['Conference'],
             'HONS': ['Honours', 'Hons']}

faculty_key = {
    'Academic Pathway Programs': ['accelerate', 'preparation'],
    'Arts and Humanities': ['justice', 'arts', 'counselling', 'criminology', 'design', 'communication', 'media',
                            'social', 'youth', 'broadcasting', 'psychotherapy', 'studies', 'psychology'],
    'Business and Law': ['commerce', 'hospitality', 'laws', 'tourism', 'sport', 'recreation',
                         'digital', 'marketing', 'advertising', 'business', 'entrepreneurship',
                         'innovation', 'human resource', 'project', 'management', 'supply chain',
                         'logistics', 'finance', 'banking', 'accounting'],
    'Education': ['education', 'teaching', 'childhood', 'primary', 'secondary', 'advanced'],
    'Engineering': ['aviation', 'chemical', 'civil', 'engineering', 'electrical', 'systems',
                    'power', 'aeronautical', 'technology'],
    'Graduate Research School': ['philosophy'],
    'Kurongkurl Katitjin': ['indigenous'],
    'Medical and Health Sciences': ['health', 'medical', 'biomedical', 'sports', 'exercise', 'rehabilitation',
                                    'therapy',
                                    'paramedical', 'pathology', 'neurological', 'paramedicine', 'emergency', 'hygiene',
                                    'oncology', 'nutrition', 'dietetics', 'toxicology', 'paramedic'],
    'Nursing and Midwifery': ['nursing', 'midwifery', 'ageing', 'mental', 'nurse'],
    'Science': ['computer', 'computing', 'security', 'terrorism', 'intelligence', 'information', 'science',
                'biological',
                'wildlife', 'cyber', 'environmental', 'marine', 'sustainability', 'data', 'bioinformatics'],
    'Western Australian Academy of Performing Arts': ['dance', 'live', 'music', 'acting', 'theatre', 'performing',
                                                      'performance', 'musical', 'screen'],

}