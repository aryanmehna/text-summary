# summarizer/views.py
import os
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .forms import UploadedPDFForm
from .models import UploadedPDF
from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import heapq

from summa import summarizer as summa_summarizer
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def is_valid_file_type(file):
    # Check if the file has a valid extension (text or pdf)
    valid_extensions = ['.pdf']
    file_name, file_extension = os.path.splitext(file.name)
    return file_extension.lower() in valid_extensions


def is_valid_file_size(file):
    # Check if the file size is within the limit (25 MB)
    return file.size <= 25 * 1024 * 1024  # 25 MB in bytes


def upload_and_summarize(request):
    if request.method == 'POST':
        form = UploadedPDFForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save(commit=False)  # Do not save to the database yet

            # Check file type and size before saving
            if not is_valid_file_type(uploaded_pdf.pdf_file) or not is_valid_file_size(uploaded_pdf.pdf_file):
                return HttpResponseBadRequest("Invalid file type or size")

            uploaded_pdf.save()  # Save to the database now that the file has passed checks

            # Process the uploaded PDF
            pdf_text = ""
            with open(uploaded_pdf.pdf_file.path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()

             # Summarize the text using Summa
            summary = summa_summarizer.summarize(pdf_text, ratio=0.2)  # Summarize to 20% of the original text

            return render(request, 'result.html', {'summary': summary})
    else:
        form = UploadedPDFForm()

    return render(request, 'upload.html', {'form': form})

"""
nltk.download('punkt')  # Download NLTK data
nltk.download('stopwords')  # Download NLTK stopwords

def is_valid_file_type(file):
    # Check if the file has a valid extension (text or pdf)
    valid_extensions = ['.txt', '.pdf']
    file_name, file_extension = os.path.splitext(file.name)
    return file_extension.lower() in valid_extensions

def is_valid_file_size(file):
    # Check if the file size is within the limit (25 MB)
    return file.size <= 25 * 1024 * 1024  # 25 MB in bytes

def upload_and_summarize(request):
    if request.method == 'POST':
        form = UploadedPDFForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save(commit=False)  # Do not save to the database yet

            # Check file type and size before saving
            if not is_valid_file_type(uploaded_pdf.pdf_file) or not is_valid_file_size(uploaded_pdf.pdf_file):
                return HttpResponseBadRequest("Invalid file type or size")

            uploaded_pdf.save()  # Save to the database now that the file has passed checks

            # Rest of the code for processing the uploaded PDF remains the same
            pdf_text = ""
            with open(uploaded_pdf.pdf_file.path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()

            # Tokenize the text
            sentences = sent_tokenize(pdf_text)

            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            word_frequencies = {}

            for sentence in sentences:
                words = word_tokenize(sentence.lower())
                for word in words:
                    if word.isalnum() and word not in stop_words:
                        if word not in word_frequencies:
                            word_frequencies[word] = 1
                        else:
                            word_frequencies[word] += 1

            # Calculate sentence scores based on word frequencies
            sentence_scores = {}
            for sentence in sentences:
                for word, freq in word_frequencies.items():
                    if word in sentence.lower():
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = freq
                        else:
                            sentence_scores[sentence] += freq

            # Get the summary by selecting top sentences
            summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
            summary = ' '.join(summary_sentences)

            return render(request, 'result.html', {'summary': summary})
    else:
        form = UploadedPDFForm()

    return render(request, 'upload.html', {'form': form})
"""