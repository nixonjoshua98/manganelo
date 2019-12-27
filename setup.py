from distutils.core import setup

setup(
  name          = 'manganelo',
  packages      = ['manganelo'],
  version       = '0.1',
  license       = 'MIT',        
  description   = 'Web scrapper package for the Manganelo website.',
  author        = 'Joshua Nion',                
  author_email  = 'nixonjoshua98@gmail.com', 
  url           = 'https://github.com/user/reponame',
  download_url  = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  
  keywords      = ["manga", "manganelo", "scrapper", "web"],
  
  install_requires=[
          'validators',
          'beautifulsoup4',
      ],

  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
  
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
