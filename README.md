# LaTex-Bund
PDF generator and CH Bund LaTex template for Markdown text.

## Introduction
Tasked with creating a unified structure of documentation for the Swiss Confederation, the purpose of this repository is to transform Markdown text files into pre-made LaTex templates based on the guidelines from the official Corporate Design of the Confederation (CD Bund) and Reglementation 52.002 (Militärische Schriftstücke), in order to output a PDF file that is in accordance with the aforementioned guidelines.

## Pre-requisites
* **Python 3.x**
  
  The main scripting language used in this project. You can download it from [python.org](https://python.org).
  
* **Pandoc**

  A universal document converter used to transform markdown and other formats.
  [Installation instructions](https://pandoc.org/installing.html).
  
* **Jinja2**

  A templating engine for Python used to render dynamic content. Install via pip:

  ``pip install Jinja2``

* **LaTex compiler**

  Required for compiling ``.tex`` files into PDF.

  * Linux: Install TeX Live via your package manager (e.g.: ``sudo apt install texlive-full``)
 
  * Windows / Mac: Use [MiKTeX](https://miktex.org/download).


## Overview
