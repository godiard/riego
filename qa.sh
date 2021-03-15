DISTRIBUTION=$(grep ^ID= /etc/os-release | awk -F '=' '{print $2}')

if [ $DISTRIBUTION == 'fedora' ]
then
   pycodestyle-3 *.py
   pyflakes-3 *.py 
else
   pep8 *.py 
   pyflakes3 *.py 
fi

