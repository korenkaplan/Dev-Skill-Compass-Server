""" this is the main entry point for scraping module"""
from logic.web_scraping.DTOS.google_jobs_configuration_dto import GoogleJobsConfigDto
from logic.web_scraping.google_jobs.google_jobs_scraping import GoogleJobsTimePeriod, \
    get_job_listings_google_jobs_pipeline
import os
from dotenv import load_dotenv
load_dotenv()

fake_jobs_list = [
    """Appsforce Is looking to talented Backend Developer who has a strong ability to work well with development
     teams and help implement solutions and results including assisting with setting standards and best practices.

A super interesting development for a Cyber Company, one of the leading companies in the world market!

Responsibilities:
• Develop, maintain, and improve the back-end components of our applications.
• Collaborate with other developers and business users to ensure that the applications meet the needs of our users.
• Work closely with Product Managers, Architects, DevOps, UI/UX, and other tech leads from our game teams.
• Write high-quality code that is efficient, secure, and well-tested.

Requirements:
• At least 4 years as Backend Developer with Python or Ruby - must
• Knowledge with Microservices architecture.
• Experience with modern CI/CD pipelines.
• Self-learning capabilities and rapid adaptation to new topics and existing software systems.""",
    """We are looking for a Python SW developer to Define, Design and Develop software infrastructure for a
     various SW Products.

What’s in it for you?

You will find yourself developing solutions to the complicated SW challenges. You will have the chance to 
innovate and develop ideas from a very early stage and shape them to make them suitable for a product.
 You'll enjoy collaborations with SW community and SW teams to integrate these technologies into Applied
  Materials next generation products.

Our group:

Backend SW group mission is to empower products SW teams to deliver new capabilities faster and better.
 We are responsible on bringing new technologies and develop SW infrastructure runway.

Key Responsibilities
• Define, Design and Develop software solutions for various SW Products
• Interface with internal and external customers
• Troubleshoot a variety of complex software issues

Skills And Experience
• BSc. in Computer Science/Computer Engineering (Universities)
• 2+ years of related experience - an advantage
• OO Java/C#/Python experience
• Kubernetes / micro services experience - an advantage
• familiar with different DB technologies - an advantage
• Experience in Python – an advantage
• Experience in multi-discipline system
• Good communication skills in Hebrew and English
• Ability to work independently as well as within a team
• Who we are?

Applied Materials Israel is home to the Process Diagnostics and Control business unit (PDC). 
Based in Rehovot, we develop, manufacture and market cutting-edge machine learning and computer vision-based
 metrology and inspection products that are essential elements in wafer fabrication. By playing a significant
  role in enabling the production of the next generation of microchips, our expertise enables our customers to 
  
  transform possibilities into reality.

Qualifications

Education:

Bachelor's Degree

Skills:

Certifications:

Languages:

Years of Experience:

4 - 7 Years

Work Experience:

Additional Information

Time Type:

Full time

Employee Type:

Assignee / Regular

Travel:

Relocation Eligible:

No

Applied Materials is an Equal Opportunity Employer committed to diversity in the workplace. All qualified applicants
 will receive consideration for employment without regard to race, color, national origin, citizenship, ancestry,
  religion, creed, sex, sexual orientation, gender identity, age, disability, veteran or military status, or any
   other basis prohibited by law""",
    """DigitalOps is seeking a Backend Developer responsible for managing the interchange of data between the server
     and the users. Your primary focus will be the development of all server-side logic, definition, and maintenance
      of the central database, and ensuring high performance and responsiveness to requests from the front end

Job Duties and Responsibilities:
• Integration of user-facing elements developed by front-end developers with server-side logic.
• Writing reusable, testable, and efficient code.
• Design and implementation of low-latency, high-availability, and performant applications.
• Implementation of security and data protection.
• Integration of data storage solutions.

Requirements, Knowledge, and Experience:
• Proven experience as a Backend Developer or similar role (3+ years).
• Bachelor's degree in Computer Science, Engineering, or related field.
• Strong proficiency with backend programming languages - Python, Node.js, C#, Java.
• Understanding of Node.js and frameworks available for it (such as Express, StrongLoop).
• Good understanding of server-side templating languages.
• Basic understanding of front-end technologies, such as HTML5, and CSS3.
• Cloud development experience using AWS & Serverless
• Experience with databases (e.g., PostgreSQL, MySQL, MongoDB), web servers.
• Understanding of accessibility and security compliance.
• User authentication and authorization between multiple systems, servers, and environments.
• Integration of multiple data sources and databases into one system.
• Management of the hosting environment, including database administration and scaling an application to 
support load changes.
• Exceptional proficiency in writing and speaking English""",
    """A universe of opportunities. Open to you.

Payoneer’s mission is to empower anyone, anywhere to participate and succeed in the global economy.
 If our mission connects with your values, if you revel in solving complex challenges, and if you want to
  continuously advance your career, come realize your potential at Payoneer!

Life at Payoneer is a global community, where you’ll work with colleagues all over the world, in a hybrid or
 remote work frame. As an equal opportunity employer, the only things that matter to us are your skills, 
 your drive, and your desire to have a positive impact on others.

Is this you?

The Payoneers are:

Accountable | Adaptable | Collaborative | Communicative | Fast Learners | Independent | Motivated |
 Problem Solvers | Resilient | Technically Proficient

What you’ll be spending your time on:
• Collaborate closely with Product, Design/UX, DevOps and other R&D teams
• Work within an autonomous team of engineers in an agile environment to achieve business goals
• Contribute to the overall design, architecture, development, code quality, and production environment 
deployment of your team
• Take an active role in defining the shape of the future of online payments
• Seize the opportunity to shape the development paradigm and capacity of our platform

Have you done this kind of stuff?
• 4+ years of experience using .Net (C#)/Java – a must!
• 2+ years of experience with relational databases such as SQL Server/Oracle/MySQL
• Thrive on working in an agile development environment
• Multi-threaded experience and understanding
• Experience developing WebAPI, REST
• Experience with messaging queues or streams such as RabbitMQ/SQS/Kafka

Not a must but a great advantage:
• Experience with Microservices app
• Experience in building SaaS platforms in a cloud environment
• Experience with distributed development, knowledge of how to make systems scale
• Experience with non-relational databases like MongoDB or others

Who we are:

Payoneer (NASDAQ: PAYO) is the world’s go-to partner for digital commerce, everywhere. 
From borderless payments to boundless growth, Payoneer promises any business, in any market, 
the technology, connections and confidence to participate and flourish in the new global economy.
 Powering growth for customers ranging from aspiring entrepreneurs in emerging markets to the world’s
  leading brands, Payoneer offers a universe of opportunities, open to you""",
    """ Backend Developer

GeoQuant is currently seeking a Backend Developer based out of Israel (hybrid).

GeoQuant is seeking to hire a Backend Developer, ideally with some background in DevOps & Infrastructure 
fields, to support the company’s tech side. Candidates will have the opportunity to code and develop in
 multiple programming languages, on a microservice oriented environment, using latest modern tech stack.

The position will work directly under GeoQuant’s Head of Technology, but will also need to communicate
 well and be able to work with other peers and senior colleagues from different departments.

What We Offer:
• GeoQuant is a non-hierarchical organization comprising a small team of driven, friendly, laid-back
 employees; the ideal candidate would possess similar qualities while also being a self-starter and
  possessing the ability to work both autonomously and at the direction of a busy executive team.
• GeoQuant’s core team is spread geographically across time zones and countries; strong time management 
and communication skills are therefore imperative.

We’ll Count on You To:
• Maintain existing code, solving bugs, implementing changes.
• Developing new features, new tools, and working on new green-field projects for new product endeavors.
• Help maintaining and keeping the stability of our infrastructure and availability of our services & products.
• Building and Improving tech-related “support systems” such as monitoring, alerts, analytics, etc.
• Supporting and helping the PoliSci team and the Sales team when working with internal (non-client facing)
 systems, usually due to clients demands.

What You Need to Have:

Academic
• BA or BsC in Computer Science, or Software Engineering, or similar degree in the field.

Technical & Professional Experience
• At least 4+ years of experience as a backend developer. Significant time working at startups or in a 
startup-like environment – advantage.
• Fluent in Ruby On Rails or NodeJS (for Backend development). Experience with the other mentioned
 language and/or Python – strong advantage
• Strong data orientation - managing and understanding data pipelines, data storage & management,
 schema design, etc. Highly experienced working with SQL (PostgreSQL – advantage). Some acquaintance 
 with MongoDB, Redis, Elasticsearch – advantage
• Regularly working using standard collaborative work practices (i.e. Git, etc…)
• Good grasp of software engineering and coding best-practices.

Must be able to deliver code at highest quality.
• At least basic familiarity with AWS Cloud Infrastructures and working with AWS management console.
• Some knowledge and experience with DevOps & Infrastructure related worlds – strong advantage.
 Specifically, with any of the following: Docker, Kubernetes, Helm, Terraform, GitOps, ArgoCD, ArgoWorkflows, Jenkins.
• Developing or maintaining algorithms implementations – advantage
• Familiar with async work distributions, workers & jobs queues, consumer-producer concept – advantage.

Languages
• Excellent verbal and written communication skills in English and Hebrew

What Would Make You Stand Out:
• Fast learner, eager to learn and expand knowledge horizontally, being a jack of many trades.
• Independent, self-sufficient, and self-reliant personality, being able to tackle big tasks with little 
spec and a lot of uncertainty and see them end to end.
• Can fill in gaps in knowledge and requirements with only little help (as opposed to being spoon-fed 
with all the nitty-gritty details)
• Must be comfortable working in dynamic agile environment (not referring to agile methodologies such
 as scrum, lean, etc, but more like “no defined methodology” work environment), where tasks and focus 
 can change frequently.
• Display exceptional organizational and time/deadline management skills and ability to prioritize 
among various deliverables.

Why Fitch?

At Fitch Group, the combined power of our global perspectives is what differentiates us. Our global network
 of colleagues comes together to accomplish things greater than they ever could alone.

Every team member is essential to our business and each perspective is critical to our success. We embrace a
 diverse culture that encourages a free exchange of ideas, guaranteeing your voice will be heard and your work
  will have an impact, regardless of seniority.

We are building incredible things at Fitch and we invite you to join us on our journey.

GeoQuant, a Fitch Solutions Company, uses advances in political and computer science to create high-frequency,
 systematic country risk data and analytics that are transparent and can be validated. Our geopolitical forecasts 
 are highly accurate because they are built on robust models. When they’re wrong, you’ll know that, too. 
 We let the data speak.

Fitch Solutions provides data, research and analytics that help clients excel at managing their credit risk,
 offer deep insight into the debt investment market and provide comprehensive intelligence macroeconomic 
 environment. All available on our platform, Fitch Connect, designed and built using our credit, macro
  and industry expertise to help you make more informed decisions.

For more information please visit our websites:

www.fitchratings.com | www.fitchsolutions.com | www.fitchlearning.com

#LI-AT

#LI-GeoQuant

#LI-Hybrid""",
    """Bigabid is an innovative technology company led by data scientists and engineers devoted to mobile
     app growth. Our proprietary ad platforms powered by machine learning are the outcome of that devotion.

We deliver valuable results and insights for a fast-growing clientele of major app developers using elite 
programmatic user acquisition and retargeting technologies.

Our ever-evolving, state-of-the-art machine learning technology analyzes tens of TB of raw data per day to 
produce millions of ad recommendations in real-time. This data is used to power our Machine Learning predictions,
 business-critical metrics, and analytics used to power our decision-making.

As a Backend Developer at Bigabid, most of your work will be centered around our proprietary bidding system 
dealing with over a million requests per second and developing our sophisticated targeting algorithms.
 You will likely face new challenges like – extreme system loads and scaling problems, working in a real-time
  environment, integrating with 3rd party platforms, and being the owner of your tasks from top to bottom.

Bigabid will give you the freedom to learn and hone your skills, allowing you the opportunity to be an
 extremely well-rounded developer where no area is off limits - stagnating is not an option.

Responsibilities:

Analyze, design, and develop new features for Bigabid’s infrastructure and product (take part in 
feature development from the requirement definition stage to final deliverable version)
• Research new development platforms, operating environments, and software solutions for 
integration or migration purposes
• Work on a low latency, high availability, large scale system.
• Produce quality products that meet high security, stability, and performance standards

Requirements:
• At least 5 years of software development experience
• Experience with C / C++, Kubernetes
• Experience with microservices architecture
• Experience with high scale
• Working with one of the cloud providers: AWS, Google, Microsoft
• Comfortable receiving code reviews, as well as giving code reviews to others
• Self-sufficient, capable of learning alone
• Can-do attitude

Bonus Skills
• Experience with real-time systems
• Experience with Redis, Aerospike, NodeJS, Typescript
• Familiarity with Agile development methodologies

Excerpt:

Face new challenges like – extreme system loads, working in a real-time environment, integrating with
 3rd party platforms, and being the owner of your tasks from top to bottom. Bigabid will give you the
  freedom to learn and hone your skills, allowing you the opportunity to be an extremely well-rounded
   developer where no area is off-limits - stagnating is not an option""",
    """We are looking for a Backend developer at Appdome.You will take part in evolving our SaaS platform into a 
    scalable product comprised of microservice components, external-facing API, and supporting a growing scale. 
    In addition, you will design our next-generation infrastructure components, improve our caching and DB use
     and transform Appdome’s SaaS into a standard platform that can support the growing customers.The code is 
     developed with NodeJs using MySQL DB, Redis, and Elasticsearch. Deployed over dockers on Kubernetes cluster
      in AWS.Responsibilities:Design, develop and deliver backend and API features in a globally distributed 
      serviceCreate microservices and enhance product scalabilityContinuously learn and evaluate new technologies
       in the everlasting effort to perfect our products""",
    """ Description

Our mission:

Digital Intelligence solutions for the public and private sectors, empowering organizations to 
master the complexities of legally sanctioned digital investigations by streamlining intelligence
 processes. Trusted by thousands of leading agencies and companies globally , Cellebrite’s Digital
  Intelligence platform and solutions transform how customers collect, review, analyze, and manage 
  investigative digital data in legally sanctioned investigations.

What is your mission?

You will learn the domain of digital intelligence while acquiring good perception of our business objectives.

We provide the necessary tools and solutions for Forensic Examiners, Police Officers, and Detectives to
 connect the dots through our technology of crime investigations, protect and save lives, accelerate 
 justice, and ensure data privacy.

You will take full ownership on leading a team in delivering features from design through implementation
 , you will be working together with stakeholders and other team leaders in order to bring great value to
  our customers.

As we modernize our tech-stack you will need to bring your experience to the whiteboard while we set our 
target-architecture and future tech roadmap.

What you’ll love about your mission?

Software developer of market leading product in Path Finder world: Path Finder Application,

Responsible for full development lifecycle from design till production phase.

Deliver high quality features with high automation coverage,

Be part of Agile Scrum multi-geographic team.

Requirements
• At least 5 years of proven success delivering high-quality distributed systems in an Agile environment.
• Proficiency in C# (Dot Net Core).
• Experience in Micro Services architecture.
• Strong experience building AWS cloud-based systems.
• Excellent critical, analytical, and problem-solving abilities.
• Superb communication skills in both Hebrew and English.

Personal Characteristics """,
    """ About Us:

Obligo’s mission is to power the rental experience of the future through trust-building financial technology that
eliminates the burden of security deposits. Renters enjoy instant qualification and deposit-free renting while 
 property owners and managers streamline their operations and make their listings more appealing to renters.

About the Position:

We are looking for a Backend Developer to join our team and take part in our high-energy TLV beach-side
 office culture.
Your primary focus will be development in a microservices infrastructure which uses the CQRS pattern, 
implementing new technologies and services, and ensuring high performance and responsiveness to requests
 from different consumers (front-end/API).
Our R&D center is based in Tel-Aviv (Geula beach!)

As a Backend Developer you will:
• Design and implement simple solutions to complicated problems
• Write high-quality, reusable and testable code
• Define and communicate technical and design requirements
• Collaborate with other developers, designers and external stakeholders
• Perform code reviews to other developers in your team

Requirements:
• 4 years of proven work experience as a Back-end developer with programming languages like Node.js, Java, and Python
• BS.c in computer science or equivalent experience
• Experience working with both NoSQL/relational databases (Mongo/Postgres/MySQL)
• Experience building dockerized services
• In-depth understanding of the entire web development process (design, development, testing and deployment)
• A team player with a can-do attitude
• Good organizational, time-management and problem-solving skills
• Experience in creating and integrating to 3rd party APIs
• Experience with AWS/GCP/Azure
• Knowledge of CQRS/event-driven design patterns - Advantage

About Obligo

Obligo is backed by VCs such as 83North, 10D and Entree capital.

The 50 most promising Israeli startups - 2024

https://www.calcalistech.com/ctechnews/article/r1f6hqqga#autoplay

Obligo 'Most Promising Israeli-Founded Fintech Startup in Lending and Financing' - Mar 2021

https://www.israelhayom.com/2021/03/23/obligo-most-promising-israeli-founded-fintech-startup-in-lending-and-financing"""
]
log_file_path = 'logic/web_scraping/Logs/web_scrape_main_run_log.txt'


# region Google Jobs Configuration
def configure_google_jobs_scrape_engine(role: str, time_period: GoogleJobsTimePeriod) -> GoogleJobsConfigDto:
    google_jobs_configuration = GoogleJobsConfigDto(
        search_value=role,
        time_period=time_period,
        show_full_description_button_xpath=os.environ.get('SHOW_FULL_DESCRIPTION_BUTTON_XPATH_GOOGLE_JOBS'),
        expandable_job_description_text_xpath=os.environ.get('EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS'),
        not_expandable_job_description_text_xpath=os.environ.get('NOT_EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS'),
        max_interval_attempts=10,
        sleep_time_between_attempt_in_seconds=30,
        wait_driver_timeout=3,
        log_file_path=log_file_path

    )
    return google_jobs_configuration


def google_jobs_scraping_pipeline(role: str, time_period: GoogleJobsTimePeriod) -> list[str]:
    # configure google jobs params
    google_jobs_config = configure_google_jobs_scrape_engine(role, time_period)

    # execute the pipeline
    job_listings: list[str] = get_job_listings_google_jobs_pipeline(google_jobs_config)

    # return the results
    return job_listings

# endregion


def job_scrape_pipeline(role: str, time_period: GoogleJobsTimePeriod) -> list[str]:
    # All jobs listings from all sites
    job_listings_list: list[str]= []

    # get the listings from Google jobs
    google_jobs_listings = google_jobs_scraping_pipeline(role, time_period)

    # add more lists from other sites...

    # combine the lists together
    job_listings_list.extend(google_jobs_listings)

    # return final result
    return job_listings_list
