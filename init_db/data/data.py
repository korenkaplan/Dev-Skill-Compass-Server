"""A module that holds Tech names in lists"""


def get_tech_set() -> set:
    tech_set = set()
    for category in _tech_list_synonyms.values():
        for synonyms in category.values():
            tech_set.update(synonyms)
    return tech_set


def get_tech_dict() -> dict:
    return _tech_list_synonyms


def get_roles_list() -> list:
    return _software_job_roles


_tech_dict = {
    'programming_languages_synonyms': [
        'javascript', 'js',
        'html', 'hypertext markup language',
        'css', 'cascading style sheets', 'css animations',
        'python', 'py',
        'sql', 'structured query language',
        'typescript', 'ts',
        'bash',
        'shell', 'shell script',
        'java',
        'c#', 'csharp', 'c-sharp',
        'c++', 'cpp', 'c plus plus',
        'c',
        'php',
        'powershell', 'pws',
        'go', 'golang',
        'rust',
        'kotlin',
        'ruby',
        'lua',
        'dart',
        'assembly', 'asm',
        'swift',
        'r',
        'visual basic (.net)', 'vb.net', 'vb',
        'matlab',
        'vba', 'visual basic for applications',
        'groovy',
        'delphi', 'object pascal',
        'scala',
        'perl', 'practical extraction and report language',
        'elixir',
        'objective-c', 'obj-c', 'objc',
        'haskell',
        'gdscript', 'godot script',
        'lisp',
        'solidity',
        'clojure', 'clj',
        'julia',
        'erlang',
        'f#', 'fsharp', 'f-sharp',
        'fortran',
        'prolog',
        'zig',
        'ada',
        'ocaml', 'objective caml',
        'apex',
        'cobol', 'common business-oriented language',
        'sas', 'statistical analysis system',
        'crystal',
        'nim',
        'apl', 'a programming language',
        'flow',
        'raku', 'perl 6'
    ],
    'databases': [
        'postgresql', 'postgres', 'pgsql',
        'mysql', 'my sql',
        'sqlite', 'sqlite3',
        'mongodb', 'mongo',
        'microsoft sql server', 'mssql', 'ms sql server', 'sql server',
        'redis',
        'mariadb', 'maria db',
        'elasticsearch', 'elastic search', 'es',
        'oracle', 'oracle db',
        'dynamodb', 'dynamo',
        'firebase realtime database', 'firebase rtdb',
        'cloud firestore', 'firestore',
        'bigquery', 'big query', 'bq',
        'microsoft access', 'ms access',
        'h2', 'h2 database',
        'cosmos db', 'azure cosmos db',
        'supabase',
        'influxdb', 'influx',
        'cassandra',
        'snowflake',
        'neo4j', 'neo 4j',
        'ibm db2', 'db2',
        'solr', 'apache solr',
        'firebird',
        'couchdb', 'couch db',
        'clickhouse',
        'cockroachdb', 'cockroach db',
        'couchbase',
        'duckdb', 'duck db',
        'datomic',
        'ravendb', 'raven db',
        'tidb', 'ti db'
    ],
    'cloud_platforms': [
        'amazon web services (aws)', 'aws', 'amazon aws',
        'microsoft azure', 'azure',
        'google cloud', 'gcp', 'google cloud platform',
        'firebase',
        'cloudflare',
        'digital ocean', 'digitalocean',
        'heroku',
        'vercel',
        'netlify',
        'vmware',
        'hetzner',
        'linode', 'now akamai', 'akamai',
        'managed hosting',
        'ovh',
        'oracle cloud infrastructure (oci)', 'oci', 'oracle cloud',
        'openshift',
        'fly.io', 'fly io',
        'vultr',
        'render',
        'openstack',
        'ibm cloud or watson', 'ibm cloud', 'watson',
        'scaleway',
        'colocation', 'colo'
    ],
    'web_frameworks': [
        'node.js', 'nodejs', 'node', 'ts-Node',
        'react', 'react.js', 'reactjs',
        'jquery',
        'express', 'express.js', "expressjs",
        'angular', 'angular.js', 'angularjs',
        'next.js', 'nextjs', 'next',
        'asp.net core', 'aspnet core', 'aspnetcore', 'dotnet core', '.net core', '.net',
        'vue.js', 'vuejs', 'vue',
        'wordpress',
        'asp.net', 'aspnet',
        'flask',
        'spring boot', 'springboot',
        'django',
        'laravel',
        'fastapi',
        'svelte',
        'ruby on rails', 'rails', 'ror',
        'nestjs', 'nest.js', 'nest',
        'blazor',
        'nuxt.js', 'nuxtjs', 'nuxt',
        'symfony',
        'deno',
        'gatsby',
        'fastify',
        'phoenix',
        'drupal',
        'codeigniter',
        'solid.js', 'solidjs', 'solid',
        'remix',
        'elm',
        'play framework',
        'lit',
        'qwik',
        'RxJS',
        'webgl',
    ],
    'other_frameworks': [
        'scikit-learn', 'scikit', 'sklearn',
        'flutter',
        'torch/pytorch', 'torch', 'pytorch',
        'react native',
        'opencv',
        'electron',
        'opengl',
        'qt',
        'cuda',
        'keras',
        'apache spark', 'spark',
        'swiftui', 'swift ui',
        'xamarin',
        'ionic',
        'hugging face transformers', 'transformers',
        'gtk',
        'cordova',
        '.net maui', 'maui',
        'hadoop',
        'tauri',
        'capacitor',
        'tidyverse',
        'quarkus',
        'ktor',
        'mfc',
        'jax',
        'micronaut',
        'uno platform'
    ],
    'other_tools': [
        'docker',
        'npm',
        'pip',
        'homebrew',
        'yarn',
        'webpack',
        'makefile',
        'kubernetes', 'k8s',
        'nuget',
        'maven (build tool)', 'maven',
        'gradle',
        'vite',
        'cmake',
        'cargo',
        'gnu gcc', 'gcc',
        'terraform',
        'msbuild',
        'ansible',
        'chocolatey',
        'composer',
        "llvm's clang", 'clang',
        'apt',
        'unity 3d', 'unity3d',
        'pacman',
        'pnpm',
        'msvc',
        'podman',
        'ninja',
        'unreal engine', 'unrealengine',
        'godot',
        'ant',
        'google test', 'gtest',
        'nix',
        'meson',
        'qmake',
        'puppet',
        'dagger',
        'chef',
        'catch2',
        'pulumi',
        'bun',
        'wasmer',
        'doctest',
        'scons',
        'bandit',
        'cppunit',
        'boost.test', 'boost test',
        'build2',
        'tunit',
        'lest',
        'snitch',
        'cute',
        'elfspy',
        'liblittletest'
    ],
    'integrated_development_environment': [
        'visual studio solution', 'visual studio code', 'vs code', 'visual studio', 'intellij idea', 'intellij',
        'notepad++',
        'notepad plus plus', 'vim', 'android studio', 'android-studio', 'pycharm', 'sublime text', 'neovim', 'neo vim',
        'eclipse', 'xcode', 'nano', 'webstorm', 'web storm', 'phpstorm',
        'atom', 'rider', 'datagrip', 'data grip', 'clion', 'ipython', 'ipy', 'emacs', 'vscodium', 'vs codium', 'goland',
        'go land', 'netbeans', 'rstudio', 'r studio', 'code::blocks', 'code blocks', 'qt creator',
        'rad studio (delphi, c++ builder)', 'rad studio', 'fleet', 'helix', 'kate', 'spyder', 'rubymine', 'ruby mine',
        'geany', 'bbedit', 'bb edit', 'textmate', 'micro', 'nova', 'condo'
    ],
    'async_tools': [
        'confluence', 'markdown file', 'markdown', 'trello', 'notion', 'github discussions',
        'azure devops', 'miro', 'wikis', 'asana', 'clickup', 'doxygen', 'redmine', 'monday.com',
        'stack overflow for teams', 'stack overflow', 'youtrack', 'microsoft planner', 'microsoft lists', 'smartsheet',
        'shortcut', 'wrike', 'adobe workfront', 'redocly', 'document360', 'nuclino', 'swit', 'dingtalk (teambition)',
        'dingtalk', 'tettra', 'workzone', 'planview projectplace or clarizen', 'planview projectplace', 'clarizen',
        'wimi', 'cerri', 'leankor'
    ],
    'synchronous_tools': [
        'microsoft teams', 'slack', 'zoom', 'discord', 'google meet', 'whatsapp', 'telegram', 'skype',
        'signal', 'google chat', 'cisco webex teams', 'webex teams', 'mattermost', 'jitsi', 'matrix', 'irc',
        'rocketchat', 'zulip', 'ringcentral', 'symphony', 'wire', 'wickr', 'unify circuit', 'coolfire core'
    ],
    'version_control_tech': [
        "git",
        "subversion (svn)", "svn",
        "mercurial", "hg",
        "perforce", "p4",
        "team foundation version control (tfvc)", "tfvc",
        "bazaar",
        "cvs (concurrent versions system)", "cvs",
        "bitbucket",
        "apache subversion",
        "github",
        "gitlab",
        "aws codecommit", "codecommit"
    ],
    'data_analyst_tools': [
        "excel",
        "tableau",
        "power bi",
        "google data studio",
        "qlikview",
        "qliksense",
        "looker",
        "seaborn",
        "plotly",
        "pandas",
        "numpy",
        "scipy",
        "spss",
        "stata",
        "jupyter notebook", "jupyter", "notebook",
        "google sheets", "google spreadsheet", "sheets",
        "redash",
        "metabase",
        "apache superset", "superset"
    ],
    'testing_and_qa_tools': [
        "jenkins",
        "travis ci",
        "circleci",
        "gitlab ci",
        "github actions",
        "teamcity",
        "bamboo",
        "azure pipelines",
        "drone",
        "concourse",
        "codeship",
        "bitbucket pipelines",
        "testrail",
        "jira",
        "zephyr",
        "practitest",
        "testlink",
        "selenium webdriver", "webdriver", "selenium",
        "appium",
        "testng",
        "test::unit",
        "unittest",
        "cucumber",
        "postman",
        "soapui",
        "rest-assured",
        "newman",
        "karate dsl",
        "blazemeter",
        "testim",
        "mabl",
        "ranorex",
        "webdriverio",
        "cypress",
        "jasmine",
        "mocha",
        "pytest",
        "junit",
        "robot framework",
        "tricentis tosca",
        "loadrunner",
        "gatling",
        "locust",
        "applitools eyes",
        "percy",
        "backstopjs",
        "galen framework",
        "wraith"
    ],
    'data_exchange_apis_and_tools': [
        "json",
        "xml",
        "restful", "rest api", "rest", "restful api", "restful apis", 'api', 'apis',
        "soap",
        "graphql",
        "protobuf",
        "protocol buffers",
        "avro",
        "thrift",
        "grpc",
        "odata",
        "hal",
        "hypertext application language",
        "json-ld",
        "linked data",
        "swagger",
        "openapi specification",
        "raml",
        "restful api modeling language",
        "oas",
        "insomnia"
    ],
    'messaging_queues_tech': [
        "mqtt",
        "amqp",
        "rabbitmq",
        'apache kafka', 'kafka',
        "apache activemq",
        "amazon sqs",
        "google cloud pub/sub",
        "gcp pub/sub",
        "azure service bus",
        "redis pub/sub",
        "zeromq",
        "nats",
        "ibm mq",
        "rocketmq",
        "nsq",
        "beanstalkd"
    ],
    'methodologies': [
        "waterfall",
        "agile",
        "scrum",
        "kanban",
        "extreme programming (xp)",
        "xp",
        "lean",
        "devops",
        "ci/cd",
        "continuous deployment",
        "spiral",
        "rapid application development (rad)",
        "rad",
        "feature driven development (fdd)",
        "fdd",
        "dynamic systems development method (dsdm)",
        "dsdm",
        "six sigma",
        "prince2",
        "itil (information technology infrastructure library)",
        "itil",
        "scaled agile framework (safe)",
        "disciplined agile (da)"
    ],
    'code_architecture': [
        "design patterns",
        "software architecture",
        "clean code",
        "modular design",
        "component-based architecture",
        "microservices",
        "monolithic",
        "event-driven",
        "soa",
        "layered",
        "hexagonal",
        "ddd",
        "mvc", "model view controller",
        "mvvm", "model view view model",
        "dependency injection",
        "ioc", "inversion of control",
        "srp", "single responsibility principle",
        "ocp", "open/closed principle",
        "lsp", "liskov substitution principle",
        "isp", "interface segregation principle",
        "dip", "dependency inversion principle"
    ],
    'top_libraries': [
        # Python
        "matplotlib",
        "tensorflow",
        "requests",
        "beautifulsoup4", "bs4",
        "sqlalchemy",
        "nltk",
        "spacy",
        "opencv-python",
        "scrapy",
        "lxml",
        "pyppeteer",
        "celery",
        "wTForms",
        "marshmallow",
        "nose",
        "coverage",
        "tox",
        "mypy",
        "pylint",
        "flake8",

        # JavaScript
        "three.js", "threejs",
        'lottie',
        'svg',
        "axios",
        "babel",
        "lodash",
        "moment",
        "gulp",
        "grunt",
        "rollup",
        "socket.io",
        "rxjs",
        "redux",
        "vuex",

        # Java
        "spring-boot",
        "hibernate",
        "log4j",
        "guava",
        "gson",
        "apache-commons",
        "jackson",
        "slf4j",
        "lombok",
        "jpa",

        # C#
        "entity-framework",
        "nunit",
        "moq",
        "nlog",
        "log4net",
        "newtonsoft-json",
        "dapper",
        "serilog",
        "signalr",
        "automapper",
        "castle-windsor",
    ],
    'protocols': [
        "http", "https", "ftp", "sftp", "ssh", "smtp", "imap", "pop3", "tcp", "udp", "ip", "ssl", "tls", "ws", "wss"
    ],
    'amazon_tech': [
        "ec2",
        "ec3",
        "s3",
        "lambda",
        "rds",
        "elastic beanstalk",
        "ecs",
        "eks",
        "fargate",
        "cloudformation",
        "cloudwatch",
        "iam",
        "vpc",
        "route 53",
        "api gateway",
        "elasticsearch service",
        "redshift",
        "athena",
        "glue",
        "kinesis",
        "sqs",
        "sns",
        "ses",
        "cognito",
        "step functions",
        "appsync",
        "codedeploy",
        "codepipeline",
        "x-ray",
        "aurora",
        "transcribe",
        "comprehend",
        "rekognition",
        "polly",
        "lex",
        "translate",
        "forecast",
        "personalize",
        "textract",
        "iot"
    ],
    'operating_systems': [
        "linux",
        "ubuntu",
        "centos",
        "redhat",
        "debian",
        "fedora",
        "windows",
        "macos",
        "ios",
        "android"
    ],
    'general_phrases': ['etl', 'data warehouse', 'columnar database', 'columnar databases', 'ux/ui',
                        'ci/cd pipelines', 'saas', 'b2b', 'e2e', 'mern', 'mean stack'],
    'security': ['oauth', 'jwt', 'jason web token', 'jason web tokens']
}
_tech_list_synonyms = {
    'programming_languages': {
        'javascript': ['javascript', 'js'],
        'html': ['html', 'hypertext markup language'],
        'css': ['css', 'cascading style sheets', 'css animations'],
        'python': ['python', 'py'],
        'sql': ['sql', 'structured query language'],
        'typescript': ['typescript', 'ts'],
        'bash': ['bash'],
        'shell': ['shell', 'shell script'],
        'java': ['java'],
        'c#': ['c#', 'csharp', 'c-sharp'],
        'c++': ['c++', 'cpp', 'c plus plus'],
        'c': ['c'],
        'php': ['php'],
        'powershell': ['powershell', 'pws'],
        'go': ['go', 'golang'],
        'rust': ['rust'],
        'kotlin': ['kotlin'],
        'ruby': ['ruby'],
        'lua': ['lua'],
        'dart': ['dart'],
        'assembly': ['assembly', 'asm'],
        'swift': ['swift'],
        'r': ['r'],
        'visual basic (.net)': ['visual basic (.net)', 'vb.net', 'vb'],
        'matlab': ['matlab'],
        'vba': ['vba', 'visual basic for applications'],
        'groovy': ['groovy'],
        'delphi': ['delphi', 'object pascal'],
        'scala': ['scala'],
        'perl': ['perl', 'practical extraction and report language'],
        'elixir': ['elixir'],
        'objective-c': ['objective-c', 'obj-c', 'objc'],
        'haskell': ['haskell'],
        'gdscript': ['gdscript', 'godot script'],
        'lisp': ['lisp'],
        'solidity': ['solidity'],
        'clojure': ['clojure', 'clj'],
        'julia': ['julia'],
        'erlang': ['erlang'],
        'f#': ['f#', 'fsharp', 'f-sharp'],
        'fortran': ['fortran'],
        'prolog': ['prolog'],
        'zig': ['zig'],
        'ada': ['ada'],
        'ocaml': ['ocaml', 'objective caml'],
        'apex': ['apex'],
        'cobol': ['cobol', 'common business-oriented language'],
        'sas': ['sas', 'statistical analysis system'],
        'crystal': ['crystal'],
        'nim': ['nim'],
        'apl': ['apl', 'a programming language'],
        'flow': ['flow'],
        'raku': ['raku', 'perl 6']
    },
    'databases': {
        'postgresql': ['postgresql', 'postgres', 'pgsql'],
        'mysql': ['mysql', 'my sql'],
        'sqlite': ['sqlite', 'sqlite3'],
        'mongodb': ['mongodb', 'mongo'],
        'microsoft sql server': ['microsoft sql server', 'mssql', 'ms sql server', 'sql server'],
        'redis': ['redis'],
        'mariadb': ['mariadb', 'maria db'],
        'elasticsearch': ['elasticsearch', 'elastic search', 'es'],
        'oracle': ['oracle', 'oracle db'],
        'dynamodb': ['dynamodb', 'dynamo'],
        'firebase realtime database': ['firebase realtime database', 'firebase rtdb'],
        'cloud firestore': ['cloud firestore', 'firestore'],
        'bigquery': ['bigquery', 'big query', 'bq'],
        'microsoft access': ['microsoft access', 'ms access'],
        'h2': ['h2', 'h2 database'],
        'cosmos db': ['cosmos db', 'azure cosmos db'],
        'supabase': ['supabase'],
        'influxdb': ['influxdb', 'influx'],
        'cassandra': ['cassandra'],
        'snowflake': ['snowflake'],
        'neo4j': ['neo4j', 'neo 4j'],
        'ibm db2': ['ibm db2', 'db2'],
        'solr': ['solr', 'apache solr'],
        'firebird': ['firebird'],
        'couchdb': ['couchdb', 'couch db'],
        'clickhouse': ['clickhouse'],
        'cockroachdb': ['cockroachdb', 'cockroach db'],
        'couchbase': ['couchbase'],
        'duckdb': ['duckdb', 'duck db'],
        'datomic': ['datomic'],
        'ravendb': ['ravendb', 'raven db'],
        'tidb': ['tidb', 'ti db']
    },
    'cloud_platforms': {
        'amazon web services (aws)': ['amazon web services (aws)', 'aws', 'amazon aws'],
        'microsoft azure': ['microsoft azure', 'azure'],
        'google cloud': ['google cloud', 'gcp', 'google cloud platform'],
        'firebase': ['firebase'],
        'cloudflare': ['cloudflare'],
        'digital ocean': ['digital ocean', 'digitalocean'],
        'heroku': ['heroku'],
        'vercel': ['vercel'],
        'netlify': ['netlify'],
        'vmware': ['vmware'],
        'hetzner': ['hetzner'],
        'linode': ['linode', 'now akamai', 'akamai'],
        'managed hosting': ['managed hosting'],
        'ovh': ['ovh'],
        'oracle cloud infrastructure (oci)': ['oracle cloud infrastructure (oci)', 'oci', 'oracle cloud'],
        'openshift': ['openshift'],
        'fly.io': ['fly.io', 'fly io'],
        'vultr': ['vultr'],
        'render': ['render'],
        'openstack': ['openstack'],
        'ibm cloud or watson': ['ibm cloud or watson', 'ibm cloud', 'watson'],
        'scaleway': ['scaleway'],
        'colocation': ['colocation', 'colo']
    },
    'web_frameworks': {
        'node.js': ['node.js', 'nodejs', 'node', 'ts-Node'],
        'react': ['react', 'react.js', 'reactjs'],
        'jquery': ['jquery'],
        'express.js': ['express', 'express.js', 'expressjs'],
        'angular': ['angular', 'angular.js', 'angularjs'],
        'next.js': ['next.js', 'nextjs', 'next'],
        'asp.net core': ['asp.net core', 'aspnet core', 'aspnetcore', 'dotnet core', '.net core', '.net'],
        'vue.js': ['vue.js', 'vuejs', 'vue'],
        'wordpress': ['wordpress'],
        'asp.net': ['asp.net', 'aspnet'],
        'flask': ['flask'],
        'spring boot': ['spring boot', 'springboot', 'spring-boot'],
        'django': ['django'],
        'laravel': ['laravel'],
        'fastapi': ['fastapi'],
        'svelte': ['svelte'],
        'ruby on rails': ['ruby on rails', 'rails', 'ror'],
        'nestjs': ['nestjs', 'nest.js', 'nest'],
        'blazor': ['blazor'],
        'nuxt.js': ['nuxt.js', 'nuxtjs', 'nuxt'],
        'symfony': ['symfony'],
        'deno': ['deno'],
        'gatsby': ['gatsby'],
        'fastify': ['fastify'],
        'phoenix': ['phoenix'],
        'drupal': ['drupal'],
        'codeigniter': ['codeigniter'],
        'solid.js': ['solid.js', 'solidjs', 'solid'],
        'remix': ['remix'],
        'elm': ['elm'],
        'play framework': ['play framework'],
        'lit': ['lit'],
        'qwik': ['qwik'],
        'rxjs': ['RxJS'],
        'webgl': ['webgl']
    },
    'other_frameworks': {
        'scikit-learn': ['scikit-learn', 'scikit', 'sklearn'],
        'flutter': ['flutter'],
        'torch/pytorch': ['torch/pytorch', 'torch', 'pytorch'],
        'react native': ['react native'],
        'opencv': ['opencv'],
        'electron': ['electron'],
        'opengl': ['opengl'],
        'qt': ['qt'],
        'cuda': ['cuda'],
        'keras': ['keras'],
        'apache spark': ['apache spark', 'spark'],
        'swiftui': ['swiftui', 'swift ui'],
        'xamarin': ['xamarin'],
        'ionic': ['ionic'],
        'hugging face transformers': ['hugging face transformers', 'transformers'],
        'gtk': ['gtk'],
        'cordova': ['cordova'],
        '.net maui': ['.net maui', 'maui'],
        'hadoop': ['hadoop'],
        'tauri': ['tauri'],
        'capacitor': ['capacitor'],
        'tidyverse': ['tidyverse'],
        'quarkus': ['quarkus'],
        'ktor': ['ktor'],
        'mfc': ['mfc'],
        'jax': ['jax'],
        'micronaut': ['micronaut'],
        'uno platform': ['uno platform']
    },
    'other_tools': {
        'docker': ['docker'],
        'npm': ['npm'],
        'pip': ['pip'],
        'homebrew': ['homebrew'],
        'yarn': ['yarn'],
        'webpack': ['webpack'],
        'makefile': ['makefile'],
        'kubernetes': ['kubernetes', 'k8s'],
        'nuget': ['nuget'],
        'maven': ['maven (build tool)', 'maven'],
        'gradle': ['gradle'],
        'vite': ['vite'],
        'cmake': ['cmake'],
        'cargo': ['cargo'],
        'gnu gcc': ['gnu gcc', 'gcc'],
        'terraform': ['terraform'],
        'msbuild': ['msbuild'],
        'ansible': ['ansible'],
        'chocolatey': ['chocolatey'],
        'composer': ['composer'],
        'clang': ["llvm's clang", 'clang'],
        'apt': ['apt'],
        'unity 3d': ['unity 3d', 'unity3d'],
        'pacman': ['pacman'],
        'pnpm': ['pnpm'],
        'msvc': ['msvc'],
        'podman': ['podman'],
        'ninja': ['ninja'],
        'unreal engine': ['unreal engine', 'unrealengine'],
        'godot': ['godot'],
        'ant': ['ant'],
        'google test': ['google test', 'gtest'],
        'nix': ['nix'],
        'meson': ['meson'],
        'qmake': ['qmake'],
        'puppet': ['puppet'],
        'dagger': ['dagger'],
        'chef': ['chef'],
        'catch2': ['catch2'],
        'pulumi': ['pulumi'],
        'bun': ['bun'],
        'wasmer': ['wasmer'],
        'doctest': ['doctest'],
        'scons': ['scons'],
        'bandit': ['bandit'],
        'cppunit': ['cppunit'],
        'boost.test': ['boost.test', 'boost test'],
        'build2': ['build2'],
        'tunit': ['tunit'],
        'lest': ['lest'],
        'snitch': ['snitch'],
        'cute': ['cute'],
        'elfspy': ['elfspy'],
        'liblittletest': ['liblittletest']
    },
    'integrated_development_environment': {
        'visual studio solution': ['visual studio solution'],
        'visual studio code': ['visual studio code', 'vs code'],
        'visual studio': ['visual studio'],
        'intellij idea': ['intellij idea', 'intellij'],
        'notepad++': ['notepad++'],
        'notepad plus plus': ['notepad plus plus'],
        'vim': ['vim'],
        'android studio': ['android studio', 'android-studio'],
        'pycharm': ['pycharm'],
        'sublime text': ['sublime text'],
        'neovim': ['neovim', 'neo vim'],
        'eclipse': ['eclipse'],
        'xcode': ['xcode'],
        'nano': ['nano'],
        'webstorm': ['webstorm', 'web storm'],
        'phpstorm': ['phpstorm'],
        'atom': ['atom'],
        'rider': ['rider'],
        'datagrip': ['datagrip', 'data grip'],
        'clion': ['clion'],
        'ipython': ['ipython', 'ipy'],
        'emacs': ['emacs'],
        'vscodium': ['vscodium', 'vs codium'],
        'goland': ['goland', 'go land'],
        'netbeans': ['netbeans'],
        'rstudio': ['rstudio', 'r studio'],
        'code::blocks': ['code::blocks', 'code blocks'],
        'qt creator': ['qt creator'],
        'rad studio (delphi, c++ builder)': ['rad studio (delphi, c++ builder)', 'rad studio'],
        'fleet': ['fleet'],
        'helix': ['helix'],
        'kate': ['kate'],
        'spyder': ['spyder'],
        'rubymine': ['rubymine', 'ruby mine'],
        'geany': ['geany'],
        'bbedit': ['bbedit', 'bb edit'],
        'textmate': ['textmate'],
        'micro': ['micro'],
        'nova': ['nova'],
        'condo': ['condo']
    },
    'async_tools': {
        'confluence': ['confluence'],
        'markdown file': ['markdown file', 'markdown'],
        'trello': ['trello'],
        'notion': ['notion'],
        'github discussions': ['github discussions'],
        'azure devops': ['azure devops'],
        'miro': ['miro'],
        'wikis': ['wikis'],
        'asana': ['asana'],
        'clickup': ['clickup'],
        'doxygen': ['doxygen'],
        'redmine': ['redmine'],
        'monday.com': ['monday.com'],
        'stack overflow for teams': ['stack overflow for teams', 'stack overflow'],
        'youtrack': ['youtrack'],
        'microsoft planner': ['microsoft planner'],
        'microsoft lists': ['microsoft lists'],
        'smartsheet': ['smartsheet'],
        'shortcut': ['shortcut'],
        'wrike': ['wrike'],
        'adobe workfront': ['adobe workfront'],
        'redocly': ['redocly'],
        'document360': ['document360'],
        'nuclino': ['nuclino'],
        'swit': ['swit'],
        'dingtalk': ['dingtalk (teambition)', 'dingtalk'],
        'tettra': ['tettra'],
        'workzone': ['workzone'],
        'planview projectplace': ['planview projectplace or clarizen', 'planview projectplace', 'clarizen'],
        'wimi': ['wimi'],
        'cerri': ['cerri'],
        'leankor': ['leankor']
    },
    'synchronous_tools': {
        'microsoft teams': ['microsoft teams'],
        'slack': ['slack'],
        'zoom': ['zoom'],
        'discord': ['discord'],
        'google meet': ['google meet'],
        'whatsapp': ['whatsapp'],
        'telegram': ['telegram'],
        'skype': ['skype'],
        'signal': ['signal'],
        'google chat': ['google chat'],
        'cisco webex teams': ['cisco webex teams', 'webex teams'],
        'mattermost': ['mattermost'],
        'jitsi': ['jitsi'],
        'matrix': ['matrix'],
        'irc': ['irc'],
        'rocketchat': ['rocketchat'],
        'zulip': ['zulip'],
        'ringcentral': ['ringcentral'],
        'symphony': ['symphony'],
        'wire': ['wire'],
        'wickr': ['wickr'],
        'unify circuit': ['unify circuit'],
        'coolfire core': ['coolfire core']
    },
    'version_control_tech': {
        'git': ['git'],
        'svn': ['subversion (svn)', 'svn'],
        'mercurial': ['mercurial', 'hg'],
        'perforce': ['perforce', 'p4'],
        'tfvc': ['team foundation version control (tfvc)', 'tfvc'],
        'bazaar': ['bazaar'],
        'cvs': ['cvs (concurrent versions system)', 'cvs'],
        'bitbucket': ['bitbucket'],
        'apache subversion': ['apache subversion'],
        'github': ['github'],
        'gitlab': ['gitlab'],
        'aws codecommit': ['aws codecommit', 'codecommit']
    },
    'data_analyst_tools': {
        'excel': ['excel'],
        'tableau': ['tableau'],
        'power bi': ['power bi'],
        'google data studio': ['google data studio'],
        'qlikview': ['qlikview'],
        'qliksense': ['qliksense'],
        'looker': ['looker'],
        'seaborn': ['seaborn'],
        'plotly': ['plotly'],
        'pandas': ['pandas'],
        'numpy': ['numpy'],
        'scipy': ['scipy'],
        'spss': ['spss'],
        'stata': ['stata'],
        'jupyter notebook': ['jupyter notebook', 'jupyter', 'notebook'],
        'google sheets': ['google sheets', 'google spreadsheet', 'sheets'],
        'redash': ['redash'],
        'metabase': ['metabase'],
        'apache superset': ['apache superset', 'superset']
    },
    'testing_and_qa_tools': {
        'jenkins': ['jenkins'],
        'travis ci': ['travis ci'],
        'circleci': ['circleci'],
        'gitlab ci': ['gitlab ci'],
        'github actions': ['github actions'],
        'teamcity': ['teamcity'],
        'bamboo': ['bamboo'],
        'azure pipelines': ['azure pipelines'],
        'drone': ['drone'],
        'concourse': ['concourse'],
        'codeship': ['codeship'],
        'bitbucket pipelines': ['bitbucket pipelines'],
        'testrail': ['testrail'],
        'jira': ['jira'],
        'zephyr': ['zephyr'],
        'practitest': ['practitest'],
        'testlink': ['testlink'],
        'selenium webdriver': ['selenium webdriver', 'webdriver', 'selenium'],
        'appium': ['appium'],
        'testng': ['testng'],
        'test::unit': ['test::unit'],
        'unittest': ['unittest'],
        'cucumber': ['cucumber'],
        'postman': ['postman'],
        'soapui': ['soapui'],
        'rest-assured': ['rest-assured'],
        'newman': ['newman'],
        'karate dsl': ['karate dsl'],
        'blazemeter': ['blazemeter'],
        'testim': ['testim'],
        'mabl': ['mabl'],
        'ranorex': ['ranorex'],
        'webdriverio': ['webdriverio'],
        'cypress': ['cypress'],
        'jasmine': ['jasmine'],
        'mocha': ['mocha'],
        'pytest': ['pytest'],
        'junit': ['junit'],
        'robot framework': ['robot framework'],
        'tricentis tosca': ['tricentis tosca'],
        'loadrunner': ['loadrunner'],
        'gatling': ['gatling'],
        'locust': ['locust'],
        'applitools eyes': ['applitools eyes'],
        'percy': ['percy'],
        'backstopjs': ['backstopjs'],
        'galen framework': ['galen framework'],
        'wraith': ['wraith']
    },
    'data_exchange_apis_and_tools': {
        'json': ['json'],
        'xml': ['xml'],
        'restful': ['restful', 'rest api', 'rest', 'restful api', 'restful apis', 'api', 'apis'],
        'soap': ['soap'],
        'graphql': ['graphql'],
        'protobuf': ['protobuf', 'protocol buffers'],
        'avro': ['avro'],
        'thrift': ['thrift'],
        'grpc': ['grpc'],
        'odata': ['odata'],
        'hal': ['hal', 'hypertext application language'],
        'json-ld': ['json-ld', 'linked data'],
        'swagger': ['swagger'],
        'openapi specification': ['openapi specification', 'oas'],
        'raml': ['raml', 'restful api modeling language'],
        'insomnia': ['insomnia']
    },
    'messaging_queues_tech': {
        'mqtt': ['mqtt'],
        'amqp': ['amqp'],
        'rabbitmq': ['rabbitmq'],
        'kafka': ['apache kafka', 'kafka'],
        'apache activemq': ['apache activemq'],
        'amazon sqs': ['amazon sqs'],
        'google cloud pub/sub': ['google cloud pub/sub', 'gcp pub/sub'],
        'azure service bus': ['azure service bus'],
        'redis pub/sub': ['redis pub/sub'],
        'zeromq': ['zeromq'],
        'nats': ['nats'],
        'ibm mq': ['ibm mq'],
        'rocketmq': ['rocketmq'],
        'nsq': ['nsq'],
        'beanstalkd': ['beanstalkd']
    },
    'methodologies': {
        'waterfall': ['waterfall'],
        'agile': ['agile'],
        'scrum': ['scrum'],
        'kanban': ['kanban'],
        'xp': ['extreme programming (xp)', 'xp'],
        'lean': ['lean'],
        'devops': ['devops'],
        'ci/cd': ['ci/cd', 'continuous deployment'],
        'spiral': ['spiral'],
        'rad': ['rapid application development (rad)', 'rad'],
        'fdd': ['feature driven development (fdd)', 'fdd'],
        'dsdm': ['dynamic systems development method (dsdm)', 'dsdm'],
        'six sigma': ['six sigma'],
        'prince2': ['prince2'],
        'itil': ['itil (information technology infrastructure library)', 'itil'],
        'safe': ['scaled agile framework (safe)'],
        'da': ['disciplined agile (da)']
    },
    'code_architecture': {
        'design patterns': ['design patterns'],
        'software architecture': ['software architecture'],
        'clean code': ['clean code'],
        'modular design': ['modular design'],
        'component-based architecture': ['component-based architecture'],
        'microservices': ['microservices'],
        'monolithic': ['monolithic'],
        'event-driven': ['event-driven'],
        'soa': ['soa'],
        'layered': ['layered'],
        'hexagonal': ['hexagonal'],
        'ddd': ['ddd'],
        'mvc': ['mvc', 'model view controller'],
        'mvvm': ['mvvm', 'model view view model'],
        'dependency injection': ['dependency injection'],
        'ioc': ['ioc', 'inversion of control'],
        'srp': ['srp', 'single responsibility principle'],
        'ocp': ['ocp', 'open/closed principle'],
        'lsp': ['lsp', 'liskov substitution principle'],
        'isp': ['isp', 'interface segregation principle'],
        'dip': ['dip', 'dependency inversion principle']
    },
    'top_libraries': {
        # Python
        'matplotlib': ['matplotlib'],
        'tensorflow': ['tensorflow'],
        'requests': ['requests'],
        'beautifulsoup4': ['beautifulsoup4', 'bs4'],
        'sqlalchemy': ['sqlalchemy'],
        'nltk': ['nltk'],
        'spacy': ['spacy'],
        'opencv-python': ['opencv-python'],
        'scrapy': ['scrapy'],
        'lxml': ['lxml'],
        'pyppeteer': ['pyppeteer'],
        'celery': ['celery'],
        'wtforms': ['wTForms'],
        'marshmallow': ['marshmallow'],
        'nose': ['nose'],
        'coverage': ['coverage'],
        'tox': ['tox'],
        'mypy': ['mypy'],
        'pylint': ['pylint'],
        'flake8': ['flake8'],

        # JavaScript
        'three.js': ['three.js', 'threejs'],
        'lottie': ['lottie'],
        'svg': ['svg'],
        'axios': ['axios'],
        'babel': ['babel'],
        'lodash': ['lodash'],
        'moment': ['moment'],
        'gulp': ['gulp'],
        'grunt': ['grunt'],
        'rollup': ['rollup'],
        'socket.io': ['socket.io'],
        'redux': ['redux'],
        'vuex': ['vuex'],

        # Java
        'hibernate': ['hibernate'],
        'log4j': ['log4j'],
        'guava': ['guava'],
        'gson': ['gson'],
        'apache-commons': ['apache-commons'],
        'jackson': ['jackson'],
        'slf4j': ['slf4j'],
        'lombok': ['lombok'],
        'jpa': ['jpa'],

        # C#
        'entity-framework': ['entity-framework'],
        'nunit': ['nunit'],
        'moq': ['moq'],
        'nlog': ['nlog'],
        'log4net': ['log4net'],
        'newtonsoft-json': ['newtonsoft-json'],
        'dapper': ['dapper'],
        'serilog': ['serilog'],
        'signalr': ['signalr'],
        'automapper': ['automapper'],
        'castle-windsor': ['castle-windsor']
    },
    'protocols': {
        'http': ['http'],
        'https': ['https'],
        'ftp': ['ftp'],
        'sftp': ['sftp'],
        'ssh': ['ssh'],
        'smtp': ['smtp'],
        'imap': ['imap'],
        'pop3': ['pop3'],
        'tcp': ['tcp'],
        'udp': ['udp'],
        'ip': ['ip'],
        'ssl': ['ssl'],
        'tls': ['tls'],
        'ws': ['ws'],
        'wss': ['wss']
    },
    'amazon_tech': {
        'ec2': ['ec2'],
        'ec3': ['ec3'],
        's3': ['s3'],
        'lambda': ['lambda'],
        'rds': ['rds'],
        'elastic beanstalk': ['elastic beanstalk'],
        'ecs': ['ecs'],
        'eks': ['eks'],
        'fargate': ['fargate'],
        'cloudformation': ['cloudformation'],
        'cloudwatch': ['cloudwatch'],
        'iam': ['iam'],
        'vpc': ['vpc'],
        'route 53': ['route 53'],
        'api gateway': ['api gateway'],
        'elasticsearch service': ['elasticsearch service'],
        'redshift': ['redshift'],
        'athena': ['athena'],
        'glue': ['glue'],
        'kinesis': ['kinesis'],
        'sqs': ['sqs'],
        'sns': ['sns'],
        'ses': ['ses'],
        'cognito': ['cognito'],
        'step functions': ['step functions'],
        'appsync': ['appsync'],
        'codedeploy': ['codedeploy'],
        'codepipeline': ['codepipeline'],
        'x-ray': ['x-ray'],
        'aurora': ['aurora'],
        'transcribe': ['transcribe'],
        'comprehend': ['comprehend'],
        'rekognition': ['rekognition'],
        'polly': ['polly'],
        'lex': ['lex'],
        'translate': ['translate'],
        'forecast': ['forecast'],
        'personalize': ['personalize'],
        'textract': ['textract'],
        'iot': ['iot']
    },
    'operating_systems': {
        'linux': ['linux'],
        'ubuntu': ['ubuntu'],
        'centos': ['centos'],
        'redhat': ['redhat'],
        'debian': ['debian'],
        'fedora': ['fedora'],
        'windows': ['windows'],
        'macos': ['macos'],
        'ios': ['ios'],
        'android': ['android']
    },
    'general_phrases': {
        'etl': ['etl'],
        'data warehouse': ['data warehouse'],
        'columnar database': ['columnar database', 'columnar databases'],
        'ux/ui': ['ux/ui'],
        'ci/cd pipelines': ['ci/cd pipelines'],
        'saas': ['saas'],
        'b2b': ['b2b'],
        'e2e': ['e2e'],
        'mern': ['mern'],
        'mean stack': ['mean stack']
    },
    'security': {
        'oauth': ['oauth'],
        'jwt': ['jwt', 'jason web token', 'jason web tokens']
    }
}
_software_job_roles = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Mobile Developer",
    "QA Engineer/Tester",
    "Security Engineer",
    "Project Manager",
    "Product Manager",
    "UI/UX Designer",
    "Data Scientist",
    "Data Analyst",
]
