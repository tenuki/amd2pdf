@set TOC_INCLUDE_LEVEL=[2,3,4]
@set ARGS=-O -t "README document"
@cd ..
python -m amd2pdf %ARGS% %* README.md -o samples\README.sample1.pdf 
python -m amd2pdf %ARGS% %* -c samples\jasonm23-foghorn.css README.md -o samples\README.sample2.pdf
@cd samples