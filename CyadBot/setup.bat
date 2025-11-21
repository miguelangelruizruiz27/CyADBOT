@echo off
echo ============================================
echo   Instalando entorno CyADBot...
echo ============================================

REM Crear entorno virtual
python -m venv .venv

REM Activar entorno
call .venv\Scripts\activate

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo Instalando modelo spaCy...
python -m spacy download es_core_news_sm

echo ============================================
echo   Instalación completada!
echo   Para iniciar el servidor usa:
echo   .venv\Scripts\activate
echo   python app.py
echo ============================================

pause
