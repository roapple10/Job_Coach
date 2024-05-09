import os
import glob
from PyPDF2 import PdfReader


class Candidate:
    def __init__(self, candidate_name):
        self._local_files = ['data/*.txt', 'data/*.pdf']
        self._resume_source = None
        self._resume_texts = dict()

        self.candidate_name = candidate_name
        self.resume_sources = []
        self.sample_writing_style = ''

        self._discover_resume_sources()
        self._read_resume()
        self._read_sample_writing()

    @property
    def resume_source(self):
        return self._resume_source

    @resume_source.setter
    def resume_source(self, source_file):
        if source_file in self._resume_texts:
            self._resume_source = source_file
        else:
            print(f"Attempted to set invalid resume source: {source_file}")

    @property
    def resume_text(self):
        try:
            return self._resume_texts[self._resume_source]
        except KeyError:
            return "No resume source set or source file does not exist."

    def _discover_resume_sources(self):
        # Using glob to resolve the wildcard patterns
        for pattern in self._local_files:
            self.resume_sources.extend(glob.glob(pattern))
        # Automatically set the first available resume source if possible
        if self.resume_sources and self._resume_source is None:
            self._resume_source = self.resume_sources[0]

    def _read_resume(self):
        for source_file in self.resume_sources:
            if source_file.endswith('.pdf'):
                with open(source_file, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    resume_text = ''.join(page.extract_text() or '' for page in pdf_reader.pages)
            else:
                with open(source_file, 'r', encoding='utf-8') as f:
                    resume_text = f.read()

            self._resume_texts[source_file] = resume_text

    def _read_sample_writing(self):
        sample_file_path = 'data/sample_writing_style.txt'
        if os.path.exists(sample_file_path):
            with open(sample_file_path, 'r', encoding='utf-8') as sample_file:
                self.sample_writing_style = sample_file.read()