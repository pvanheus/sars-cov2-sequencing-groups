#!/usr/bin/env python

import argparse
import csv
from dataclasses import dataclass
from operator import itemgetter
from typing import TextIO
import sys


@dataclass
class seq_info:
    lab: str
    region: str
    country: str
    division: str
    authors: str

    def to_tsv(self):
        return '\t'.join([self.lab, self.region, self.country, self.division, self.authors])

def summarise_metadata(input_file: TextIO, output_file: TextIO):
    reader = csv.DictReader(input_file, delimiter="\t")
    lab_synonyms = [
        ('Al Jalila Genomics Center', 'Al Jalila Childrens Hospital'),
        ('Andersen Lab, The Scripps Research Institute', 'Andersen lab at Scripps Research'),
        ('1. Department of Medical Sciences, Ministry of Public Health, Thailand 2. Thai Red Cross Emerging Infectious Diseases - Health Science Centre 3. Department of Disease Control, Ministry of Public Health, Thailand', 'National Institute of Health. Department of medical Sciences, Ministry of Public Health, Thailand'),
        ('AIDS Vaccine Research Laboratories', 'University of Wisconsin-Madison AIDS Vaccine Research Laboratories', 'University of Wisconsin-Madison, AIDS Vaccine Research Laboratories', 'University of Wisconsin-Madison AIDS Vaccine Research Laboratory'),
        ('Al Jalila Genomics Center', 'Al Jalila Childrens Hospital'),
        ('ARGO Open Lab Platform for Genome sequencing', 'ARGO Open Lab Platform for Genome Sequencing'),
        ('Beijing Genomics Institute (BGI)', "BGI & Institute of Microbiology, Chinese Academy of Sciences & Shandong First Medical University & Shandong Academy of Medical Sciences & General Hospital of Central Theater Command of People's Liberation Army of China"),
        ('BioInfoExperts, LLC', 'Bioinfoexperts, LLC'),
        ('Bioinformatics Laboratory', 'Bioinformatics Laboratory - LNCC', 'Bioinformatics Laboratory / LNCC'),
        ('Bioinformatics Research Group, Szentagothai Research Centre', 'Bioinformatics Research Group, Szentagothai Research Centre, University of Pecs'),
        ('Center of Scientific Excellence for Influenza Viruses,National Research Centre (NRC), Egypt.', 'Center of Scientific Excellence for Influenza Viruses, National Research Centre (NRC), Egypt.'),
        ('Centers for Disease Control, R.O.C. (Taiwan)', 'Taiwan Centers for Disease Control'),
        ('Charite Universitaetsmedizin Berlin, Institute of Virology', 'Charite Universitatsmedizin Berlin, Institute of Virology'),
        ('Chinese PLA Institute for Disease Control and Prevention', 'Infectious Disease Control Center'),
        ('Chiu Laboratory, University of California, San Francisco', 'University of California, San Francisco'),
        ('Dasman diabetes Institute', 'Dasman Diabetes Institute'),
        ('Department of Laboratory Medicine, Lin-Kou Chang Gung Memorial Hospital, Taoyuan, Taiwan', 'Department of Laboratory Medicine, Lin-Kou Chang Gung Memorial Hospital, Taoyuan, Taiwan.'),
        ('Department of Medical Microbiology', 'Department of Medical Microbiology, Faculty of Medicine, University of Malaya'),
        ('Department of Microbiology, Gandhi Medical College and Hospital, Secendrabad, Hyderabad, India', 'Department of Microbiology, Gandhi Medical College and Hospital, Secendrabad, Hyderabad'),
        ('Department of Microbiology, Zhejiang Provincial Center for Disease Control and Prevention', 'Zhejiang Provincial Center for Disease Control and Prevention', 'Department of Microbiology, Gandhi Medical College and Hospital Secendrabad, Hyderbad, India'),
        ('Department of Pathology and Medicine, New York University School of Medicine', 'Departments of Pathology and Medicine, New York University School of Medicine'),
        ('Department of Virology Faculty of Medicine, Medicum University of Helsinki', 'Department of Virology, Faculty of Medicine, University of Helsinki, Helsinki, Finland'),
        ('Division of Viral Diseases, Center for Laboratory Control of Infectious Diseases, Korea Centers for Diseases Control and Prevention', 'Korea Centers for Disease Control & Prevention (KCDC) Center for Laboratory Control of Infectious Diseases Division of Viral Diseases'),
        ('Division of Consolidated Laboratory Services', 'VA DCLS'),
        ('Fuyang City Center for Disease Control and Prevention', 'Clinical Laboratory'),
        ('Chulalongkorn University Faculty of Medicine', 'Faculty of Medicine'),
        ('Guangdong Provincial Center for Disease Control and Prevention', 'Department of Microbiology, Guangdong Provincial Center for Diseases Control and Prevention'),
        ('Gujarat Biotechnology Research Centre, Gandhinagar', 'Gujarat Biotechnology Research Centre'),
        ('Hopitaux universitaires de Geneve Laboratoire de Virologie', 'University Hospitals of Geneva Laboratory of Virology'),
        ('Hangzhou Center for Diseases Control and Prevention', 'Inspection Center of Hanghzou Center for Disease Control and Prevention'),
        ('Hubei Provincial Center for Disease Control and Prevention', 'Institute of Viral Disease Control and Prevention, China CDC'),
        ('Insepction Center of Hangzhou Center for Disease Control and Prevention', 'Inspection Center of Hangzhou Center for Disease Control and Prevention'),
        ('Instituto de Diagnostico y Referencia Epidemiologicos (INDRE)', 'Instituto de Diagnostico y Referencia Epidemiologicos'),
        ('Institute for Medical Research Infectious Disease Research Centre, National Institutes of Health, Ministry of Health Malaysia', 'Institute for Medical Research, Infectious Disease Research Centre, National Institutes of Health, Ministry of Health Malaysia'),
        ('Institute information KU Leuven, Clinical and Epidemiological Virology', 'KU Leuven, Clinical and Epidemiological Virology', 'Institute information KU Leuven, Clinical and Epidemiological Virology'),
        ('Institute of Microbiology Universidad San Francisco de Quito', 'Institute of Microbiology, Universidad San Francisco de Quito'),
        ('Institute of Tropical Disease, Universitas Airlanga', 'Institute of Tropical Disease, Universitas Airlangga'),
        ('Instituto Adolfo Lutz, Interdisciplinary Procedures Center, Strategic Laboratory', 'Instituto Adolfo Lutz Interdisciplinary Procedures Center Strategic Laboratory', 'Instituto Adolfo Lutz, Interdiciplinary Procedures Center, Strategic Laboratory'),
        ('Instituto Nacional de Ciencias Medicas y Nutricion', 'Instituto Nacional de Ciencias Medicas y Nutricion Salvador Zubiran'),
        ('Instituto Nacional de Salud Universidad Cooperativa de Colombia Instituto Alexander von Humboldt Imperial College-London London School of Hygiene & Tropical Medicine', 'Instituto Nacional de Salud, Universidad Cooperativa de Colombia, Instituto Alexander von Humboldt, Imperial College-London, London School of Hygiene & Tropical Medicine'),
        ('Institut Pasteur CIBU /ERI', 'Institut Pasteur CIBU / ERI', 'Institut Pasteur CIBU-ERI'),
        ('Istituto Zooprofilattico Sperimentale dell\'Abruzzo e Molise "G. Caporale"', 'Istituto Zooprofilattico Sperimentale dellAbruzzo e Molise G. Caporale', 'Istituto Zooprofilattico Sperimentale dell\'Abruzzo e Molise "G.Caporale"'),
        ('James Molecular Lab - OSUWMC', 'The Ohio State University-James Molecular Lab at Polaris'),
        ('Jiangxi Province Center for Disease Control and Prevention', 'Jiangxi province Center for Disease Control and Prevention'),
        ('Kawsar Human Genetic Research Company', 'Human Genetic Research Center', 'Kawsar Human Genetic Research Center'),
        ('KU Leuven, Clincal and Epidemiological Virology', 'KU Leuven, Clinical and Epidemiological Virology'),
        ('Laboratoire Nationale de Sante, Microbiology, Epidemiology and Microbial Genomics', 'Laboratoire National de Sante, Microbiology, Epidemiology and Microbial Genomics'),
        ('Laboratorio de Referencia Nacional de Biotecnologia y Biologia Molecular.Instituto Nacional de Salud.Peru', 'Laboratorio de Referencia Nacional de Biotecnologia y Biologia Molecular. Instituto Nacional de Salud Peru'),
        ('Laboratory of Biology, Department of Medicine, Democritus University of Thrace', 'Laboratory of Biology, Department of Medicine, Democritus University of Thrace, Greece'),
        ('Lednicky Laboratory, Emerging Pathogens Institute, University of Florida.', 'Lednicky Laboratory at Emerging Pathogens Institute, University of Florida', 'Lednicky Laboratory, Emerging Pathogens Institute, University of Florida.'),
        ('Li Ka Shing Faculty of Medicine, The University of Hong Kong', 'Microbiology', 'unknown', 'State Key Laboratory for Emerging Infectious Diseases Department of Microbiology Li Ka Shing Faculty of Medicine The University of Hong Kong'), # the lab of To and Chan
        ('Michigan Department of Health and Human Services, Bureau of Laboratories', 'Bureau of Laboratories'),
        ('Microbial Genomics Laboratory, Institut Pasteur Montevideo', 'Microbial Genomics Laboratory, Institut Pasteur Montevideo, Uruguay'),
        ('Microbiological Diagnostic Unit Public Health Laboratory and Victorian Infectious Diseases Reference Laboratory, Doherty Institute', 'Microbiological Diagnostic Unit Public Health Laboratory and Victorian Infectious Diseases Reference Laboratory, The Peter Doherty Institute for Infection & Immunity', 'Victorian Infectious Diseases Reference Laboratory and Microbiological Diagnostic Unit Public Health Laboratory, Doherty Institute', 'Microbiological Diagnostic Unit Public Health Laboratory and Victorian Infectious Diseases Reference Laboratory, The Peter Doherty Institute for Infection and Immunity', 'Collaboration between the University of Melbourne at The Peter Doherty Institute for Infection and Immunity, and the Victorian Infectious Disease Reference Laboratory'),
        ('Molecular Infectious Disease', 'Programme in Emerging Infectious Diseases, Duke-NUS Medical School'),
        ('National Influenza Center, Indian Council of Medical Research-National Institute of Virology', 'National Influenza Center, Indian Council of Medical Research - National Institute of Virology'),
        ('National Influenza Center - National Institute of Hygiene and Epidemiology (NIHE)', 'National Influenza Center, National Institute of Hygiene and Epidemiology (NIHE)'),
        ('National Institute for Communicable Disease Control and Prevention (ICDC) Chinese Center for Disease Control and Prevention (China CDC)', 'Pathogen Discovery, Respiratory Viruses Branch, Division of Viral Diseases, Centers for Disease Control and Prevention', 'National Institute for Viral Disease Control & Prevention, CCDC', 'National Institute for Viral Disease Control and Prevention, China CDC'),
        ('National Public Health Laboratory', 'National Centre for Infectious Diseases, National Centre for Infectious Diseases', 'National Public Health Laboratory, National Centre for Infectious Diseases'),
        ('Norwegian Institute of Public Health, Department of Virology', 'Norwegian Institute of Public Health'),
        ('NSW Health Pathology - Institute of Clinical Pathology and Medical Research; Centre for Infectious Diseases and Microbiology Laboratory Services; Westmead Hospital; University of Sydney', 'NSW Health Pathology - Institute of Clinical Pathology and Medical Research; Westmead Hospital; University of Sydney'),
        ('Microbiology and Immunology department, Pasteur institute in Ho Chi Minh city', '	Microbiology and Immunology department'),
        ('PathWest Laboratory Medicine WA', 'Department of Microbiology, PathWest QEII Medical Centre'),
        ('Philippine Genome Center', 'Philippine Genome Center, University of the Philippines System'),
        ('Public Health Ontario Laboratories', 'Ontario Agency for Health Protection and Promotion (OAHPP)'),
        ('Public Health Virology Laboratory, Forensic and Scientific Services, Queensland Health', 'Public Health Virology Laboratory, Forensics and Scientific Services, Queensland Health'),
        ('R. G. Lugar Center for Public Health Research, National Center for Disease Control and Public Health (NCDC) of Georgia.', 'Department for Virology, Molecular Biology and Genome Research, R. G. Lugar Center for Public Health Research, National Center for Disease Control and Public Health (NCDC) of Georgia.'),
        ('School of Public Health, The University of Hong Kong', 'School of Public Health, The University of Hon g Kong', 'The University of Hong Kong'),
        ('Sequencing and Bioinformatics Service and Molecular Epidemiology Research Group. FISABIO-Public Health.', 'Sequencing and Bioinformatics Service and Molecular Epidemiology Research Group. FISABIO-Public Health', 'Sequencing and Bioinformatics Service. Molecular Epidemiology Laboratory. FISABIO-Public Health', 'Sequencing and Bioinformatics Service FISABIO-Public Health'),
        ("Shenzhen Key Laboratory of Pathogen and Immunity, National Clinical Research Center for Infectious Disease, Shenzhen Third People's Hospital", "Shenzhen Key Laboratory of Pathogen and Immunity, National Clinical Research Center for Infectious Disease,Shenzhen Third People's Hospital"),
        ('State Key Laboratory for Diagnosis and Treatment of Infectious Diseases, National Clinical Research Center for Infectious Diseases, First Affiliated Hospital, Zhejiang University School of Medicine, Hangzhou, China 310003', 'State Key Laboratory for Diagnosis and Treatment of Infectious Diseases, National Clinical Research Center for Infectious Diseases, First Affiliated Hospital, Zhejiang University School of Medicine, Hangzhou, China. 310003'),
        ('State Veterinary Institute Prague', 'The National Institute of Public Health Center for Epidemiology and Microbiology'),
        ('Takayuki Hishiki Kanagawa Prefectural Institute of Public Health', 'Takayuki Hishiki Kanagawa Prefectural Institute of Public Health, Department of Microbiology'),
        ('Thai National Influenza Center, Department of medical Science, Ministry of Public Health, Thailand', 'National Institute of Health. Department of medical Sciences, Ministry of Public Health, Thailand'),
        ('the First Affiliated Hospital of Guangzhou Medical University & BGI-Shenzhen', 'The First Affiliated Hospital of Guangzhou Medical University & BGI-Shenzhen'),
        ('The Ohio State University James Molecular lab', 'The Ohio State University-James Molecular Lab at Polaris'),
        ('University Hospital Basel, Clinical Bacteriology', 'University Hospital Basel, Labormedizin', 'University Hospital Basel, Clinical Bacteriology'),
        ('Onderzoeksgroep Virologie, University Hospital Gent', 'Onderzoeksgroep Virologie'),
        ('University Hospitals of Geneva Laboratory of Virology', 'Hopitaux universitaires de Geneve Laboratoire de Virologie'),
        ('University of California, San Francisco', 'Chiu Laboratory, University of California, San Francisco'),
        ('University of Washington Virology Lab', 'UW Virology Lab'),
        ('University of Wisconsin-Madison AIDS Vaccine Research Laboratories', 'AIDS Vaccine Research Laboratories', 'University of Wisconsin - Madison AIDS Vaccine Research Laboratories', 'University of Wisconsin-Madison, AIDS Vaccine Research Laboratories'),
        ('ViFU', 'Statens Serum Institute'),
        ('Virus Research Laboratory, Department of Zoology, Osmania University, Hyderabad, India', 'Virus Research Laboratory, Department of Zoology, Osmania University,Hyderabad,India'),
        ('Wadsworth Center, New York State Department.of Health', 'Wadsworth Center, New York State Department of Health'),
    ]
    lab_synonyms_dict = {}
    for synonyms in lab_synonyms:
        for name in synonyms[1:]:
            lab_synonyms_dict[name] = synonyms[0]
    labs = set()
    lab_list = []
    for row in reader:
        submitting_lab = row["submitting_lab"]
        authors = row["authors"]
        region = row["region"]
        country = row["country"]
        division = row["division"]
        lab_name = lab_synonyms_dict.get(submitting_lab, submitting_lab)
        lab_key = (lab_name, country, region)
        if lab_key in labs:
            continue
        labs.add(lab_key)
        lab_info = seq_info(
            lab=lab_name,
            country=country,
            region=region,
            division=division,
            authors=authors,
        )
        lab_list.append(lab_info)

    for lab in sorted(lab_list, key=lambda x: '|'.join([x.region, x.country, x.division, x.lab])):
        print(lab.to_tsv())
        # pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarise metadata from GISAID")
    parser.add_argument(
        "input_file", type=argparse.FileType(), help="Input file with GISAID metadata"
    )
    parser.add_argument("output_file", nargs="?", default=sys.stdout)
    args = parser.parse_args()

    summarise_metadata(args.input_file, args.output_file)
