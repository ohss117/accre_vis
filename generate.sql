CREATE VIRTUAL TABLE school_names_fts using fts4(INSTITUTION_NAME TEXT, tokenize='porter')();
INSERT INTO SCHOOL_NAMES_FTS SELECT INSTITUTION_NAME FROM ACCREDITATION_2015_6 GROUP BY INSTITUTION_NAME;