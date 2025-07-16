\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bundreport-short}[2025/07/15 Bund report short - Marcos Cabanas]

% --- Load base class ---
\LoadClass{classes/bundreport-full}

% --- NEW FRONT PAGE BLOCK ---
% Custom title block for short reports
\newcommand{\shortreporttitleblock}{
  \thispagestyle{empty} % suppress headers/footers
  \begin{textblock*}{160mm}(30mm,30mm)
    \includegraphics[width=50mm]{logos/logo_bund.png}
  \end{textblock*}

  \begin{textblock*}{160mm}(30mm,60mm)
    \fontsize{18}{22}\selectfont \textbf{\reporttitle}
  \end{textblock*}

  \begin{textblock*}{160mm}(30mm,80mm)
    \fontsize{12}{14}\selectfont \reportsubtitle
  \end{textblock*}

  \begin{textblock*}{160mm}(30mm,100mm)
    \fontsize{10}{12}\selectfont \reportauthor
  \end{textblock*}

  \begin{textblock*}{160mm}(30mm,110mm)
    \fontsize{10}{12}\selectfont \reportdate
  \end{textblock*}
}

% --- Replace the shield graphic with a blank file ---
\usepackage{graphicx}
\makeatletter
\def\@shieldfile{logos/shield_bund.png}
\def\@blankfile{logos/blank.png}
% Store the original \includegraphics command
\let\origincludegraphics\includegraphics
\DeclareRobustCommand{\includegraphics}[2][]{%
  \begingroup
    \edef\@tempa{#2}%
    \edef\@shieldtest{\@shieldfile}%
    \ifx\@tempa\@shieldtest
      \origincludegraphics[#1]{\@blankfile}%
    \else
      \origincludegraphics[#1]{#2}%
    \fi
  \endgroup
}
\makeatother

% --- Geometry for new mainmatter header ---
\geometry{
  top=25mm,         % body text top
  headheight=0mm,
  headsep=13mm      % classification will be at 12mm from top (25 - 13)
}

% --- Remove report number from the header ---
\makeatletter
\renewcommand{\setstandardpagestyle}{%
  \fancypagestyle{standard}{%
    \fancyhf{}%
    \fancyhead[R]{\vspace*{-1mm}\fontsize{10}{13}\selectfont \textbf{\classification}}%
  }%
  \pagestyle{standard}
  \inmainmattertrue
}
\makeatother

% Define the header and footer packages
\usepackage{atbegshi,textpos,lastpage}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\textblockorigin{0mm}{0mm}

% Keep page number and add a rule
\makeatletter
\AtBeginShipout{%
  \ifinmainmatter
    \ifnum\value{page}>0\relax % Skip overlays on first page
      \AtBeginShipoutUpperLeft{%
        % Horizontal line above footer
        \begin{textblock*}{164mm}(30mm,277mm)
          \noindent\rule{164mm}{0.4pt}
        \end{textblock*}
        % Footer: report title on left, page number on right
        \begin{textblock*}{160mm}(30mm,278mm)
          \fontsize{9}{11}\selectfont \reporttitle
        \end{textblock*}

        \begin{textblock*}{0mm}[1,0](190mm,278mm)
          \fontsize{7}{10}\selectfont \thepage/\pageref{LastPage}
        \end{textblock*}
      }%
    \fi
  \fi
}
\makeatother