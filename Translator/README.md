# translator

We can run this project in both colab(Recommended) and local. Run in colab for faster translation.

Colab:
1. Login and create new notebook in colab
2. Clone git project into colab or copy paste and run below command
!git clone https://github.com/ashokv22/translator.git
3. Run run.sh file as below to download required libraries and trained language model. This may take a while.
!cd /content/translator && bash -x /content/translator/run.sh
4. After installation of required libraries, flask-ngrok will generate random ip address. 
Click on it will redirect to new tab and open's the index page.
5. Now you can translate the text.
6. If it gives error detect language run !pip install detectlanguage
