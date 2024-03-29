%%% This class is based on the ShareLaTeX template "Programming Assignment" (https://www.sharelatex.com/templates/other/programming-assignment) which is a modified version of the template originally created by Karol Kozioł (mail@karol-koziol.net)
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{prog_report}[2016/01/11 Programming Report based on ShareLaTeX template]

\LoadClass[a4paper,11pt]{article}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{xcolor}

\usepackage{url}
\usepackage[hypcap]{caption}
% Clickable hyperlinks: Should be loaded as late as possible
% Pass hyphens options to automatically break long urls. Use PassOptionsToPackage to ensure correct passing to transitively loaded url package
\PassOptionsToPackage{hyphens}{url}\usepackage{hyperref}
% Deals with encodings in the .out file; Load directly after hyperref
\usepackage{bookmark}

\renewcommand\familydefault{\sfdefault}
\usepackage{tgheros}
\usepackage[defaultmono]{droidmono}

% Incompatible with hyperref if using \label{...}
% See http://tex.stackexchange.com/questions/130319/incompatibility-between-etoolbox-and-hyperref
%\usepackage{amsmath}
\usepackage{amssymb,amsthm,textcomp}
\usepackage{enumerate}
\usepackage{multicol}
\usepackage{tikz}

\usepackage{geometry}
\geometry{total={210mm,297mm},
left=25mm,right=25mm,%
bindingoffset=0mm, top=20mm,bottom=20mm}


\linespread{1.3}

%%% Custom commands
\newcommand{\linia}{\rule{\linewidth}{0.5pt}}
\newcommand{\code}[1]{\texttt{#1}}

% custom theorems if needed
%\newtheoremstyle{mytheor}
%    {1ex}{1ex}{\normalfont}{0pt}{\scshape}{.}{1ex}
%    {{\thmname{#1 }}{\thmnumber{#2}}{\thmnote{ (#3)}}}
%
%\theoremstyle{mytheor}
%\newtheorem{defi}{Definition}

% my own titles
\makeatletter
\renewcommand{\maketitle}{
\begin{center}
\vspace{2ex}
{\huge \textsc{\@title}}
\vspace{1ex}
\\
\linia\\
\@author \hfill \@date
%\@email
\vspace{4ex}
\end{center}
}
\makeatother
%%%

% custom footers and headers
\usepackage{fancyhdr}
\pagestyle{fancy}
\lhead{}
\chead{}
\rhead{}
\lfoot{}
\cfoot{}
\rfoot{Page \thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% code listing settings
\usepackage{listings}
\lstset{
    language=Haskell,
    basicstyle=\ttfamily\small,
    aboveskip={1.0\baselineskip},
    belowskip={1.0\baselineskip},
    columns=fixed,
    extendedchars=true,
    breaklines=true,
    tabsize=4,
    prebreak=\raisebox{0ex}[0ex][0ex]{\ensuremath{\hookleftarrow}},
    frame=lines,
    showtabs=false,
    showspaces=false,
    showstringspaces=false,
    keywordstyle=\color[rgb]{0.627,0.126,0.941},
    commentstyle=\color[rgb]{0.133,0.545,0.133},
    stringstyle=\color[rgb]{01,0,0},
    numbers=left,
    numberstyle=\small,
    stepnumber=1,
    numbersep=10pt,
    captionpos=t,
    escapeinside={\%*}{*)}
}
