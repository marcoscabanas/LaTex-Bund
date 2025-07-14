\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bundreport}[2025/07/14 Bund report - Marcos Cabanas]

% --- LOAD BASE CLASS ---
\LoadClass[11pt,a4paper]{article}

% --- REQUIRED PACKAGES ---
\RequirePackage[
  a4paper,
  top=48mm,        % To place header content (8.3mm sep + 39.7mm target)
  headheight=13mm,  % Header box height
  headsep=8.3mm,   % Distance between header box and body
  left=30mm,
  textwidth=160mm,
  bottom=28mm      % Ensures footer lands at 281mm
]{geometry}
\addtolength{\topmargin}{-13pt}
\RequirePackage{changepage}
\RequirePackage[absolute,overlay]{textpos}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\textblockorigin{0mm}{0mm}
\RequirePackage{lastpage}
\RequirePackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\RequirePackage{graphicx}
\RequirePackage{fancyhdr}
\RequirePackage{anyfontsize}
\RequirePackage{titlesec}
\RequirePackage{enumitem}
\setlist[itemize]{left=2cm}
\setlist[enumerate]{left=2cm}
\RequirePackage{atbegshi}
\RequirePackage{float}

% --- SECTION TITLE SPACING FORMATTING ---
\titleformat{\section}
  {\normalfont\large\bfseries}
  {\thesection}
  {17.5mm}
  {}

\titleformat{\subsection}
  {\normalfont\large\bfseries}
  {\thesubsection}
  {14.1mm}
  {}

\titleformat{\subsubsection}
  {\normalfont\large\bfseries}
  {\thesubsubsection}
  {10.6mm}
  {}

\newcommand{\setmainmatterindent}{
  \setlength{\leftskip}{20mm}
  \setlength{\parindent}{0pt}
}


% --- REPORT METADATA COMMANDS ---
% Relevant department
\newcommand{\setrelevantdepartment}[1]{\def\@relevantdepartment{#1}}
\newcommand{\relevantdepartment}{\@relevantdepartment}
\newcommand{\@relevantdepartment}{} % initialize

% Relevant section
\newcommand{\setrelevantsection}[1]{\def\@relevantsection{#1}}
\newcommand{\relevantsection}{\@relevantsection}
\newcommand{\@relevantsection}{} % initialize

% Report title
\newcommand{\setreporttitle}[1]{\def\@reporttitle{#1}}
\newcommand{\reporttitle}{\@reporttitle}
\newcommand{\@reporttitle}{} % initialize

% Report subtitle
\newcommand{\setreportsubtitle}[1]{\def\@reportsubtitle{#1}}
\newcommand{\reportsubtitle}{\@reportsubtitle}
\newcommand{\@reportsubtitle}{} % initialize

% Report number
\newcommand{\setreportnumber}[1]{\def\@reportnumber{#1}}
\newcommand{\reportnumber}{\@reportnumber}
\newcommand{\@reportnumber}{} % initialize

% Classification
\newcommand{\setclassification}[1]{\def\@classification{#1}}
\newcommand{\classification}{\@classification}
\newcommand{\@classification}{} % initialize

% Report author
\newcommand{\setreportauthor}[1]{\def\@reportauthor{#1}}
\newcommand{\reportauthor}{\@reportauthor}
\newcommand{\@reportauthor}{} % initialize

% Report date
\newcommand{\setreportdate}[1]{\def\@reportdate{#1}}
\newcommand{\reportdate}{\@reportdate}
\newcommand{\@reportdate}{} % initialize

% QR code reference
\newcommand{\setqrcodereference}[1]{\def\@qrcodereference{#1}}
\newcommand{\qrcodereference}{\@qrcodereference}
\newcommand{\@qrcodereference}{} % initialize

% --- MAIN MATTER PAGE STYLE ---
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Overlays for shield and footer
\newif\ifinmainmatter
\inmainmatterfalse

% Setting the header
\newcommand{\setstandardpagestyle}{
  \fancypagestyle{standard}{
    \fancyhf{}
    \fancyhead[L]{\fontsize{7.5}{10}\selectfont \reportnumber}
    \fancyhead[R]{\fontsize{10}{13}\selectfont \textbf{\classification}}
  }
  \inmainmattertrue
}

% Shield and page number positioning
\AtBeginShipout{%
  \ifinmainmatter
    \AtBeginShipoutUpperLeft{%
      \begin{textblock*}{55mm}(13mm,12mm)
        \includegraphics[width=55mm]{logos/shield_bund.png}
      \end{textblock*}
      \begin{textblock*}{0mm}[1,0](190mm,278mm) % calculated manually such that bottom of footer ligns up with 281mm.
        \fontsize{7}{10}\selectfont \thepage/\pageref{LastPage}
      \end{textblock*}
    }%
  \fi
}

% --- FLAGS TO TRACK PREVIOUS HEADING LEVEL ---
\newif\ifaftersection
\newif\ifaftersubsection
\newif\ifaftersubsubsection
\aftersectionfalse
\aftersubsectionfalse
\aftersubsubsectionfalse

% --- PATCH SECTION ---
\let\oldsection\section
\renewcommand{\section}[1]{%
  \ifaftersubsection
    \vspace{\baselineskip}
  \fi
  \ifaftersubsubsection
    \vspace{\baselineskip}
  \fi
  \aftersectiontrue
  \aftersubsectiontrue
  \aftersubsubsectiontrue
  \oldsection{#1}%
}


% --- PATCH SUBSECTION ---
\let\oldsubsection\subsection
\renewcommand{\subsection}[1]{%
  % Insert spacing if previous was section
  \ifaftersection
    \vspace{\baselineskip}
  \fi
  \aftersectiontrue
  \aftersubsectiontrue
  \aftersubsubsectionfalse
  \oldsubsection{#1}%
}

% --- PATCH SUBSUBSECTION ---
\let\oldsubsubsection\subsubsection
\renewcommand{\subsubsection}[1]{%
  % Insert spacing if previous was subsection
  \ifaftersubsection
    \vspace{\baselineskip}
  \fi
  \aftersubsectiontrue
  \oldsubsubsection{#1}%
}

\titlespacing*{\section}
  {0mm}
  {0mm}
  {0mm}

\titlespacing*{\subsection}
  {0mm}
  {0mm}
  {0mm}

\titlespacing*{\subsubsection}
  {0mm}
  {0mm}
  {0mm}

% --- PANDOC COMPATIBILITY PATCHES ---
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
