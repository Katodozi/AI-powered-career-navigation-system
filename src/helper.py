from typing import List
import re


def extract_skills_from_description(description: str) -> List[str]:
    if not description:
        return []

    skill_keywords = [
    # === DEVELOPMENT FRAMEWORKS & LANGUAGES (68) ===
    "Node.js", "React", "React Native", "Vue.js", "Angular", "AngularJS", "Flutter", "Dart", 
    ".NET", ".NET Core", "C#", "JavaScript", "TypeScript", "HTML", "HTML5", "CSS", "CSS3", 
    "GraphQL", "REST APIs", "RESTful APIs", "NestJS", "Express.js", "Next.js", "Laravel", 
    "Wordpress", "Swift", "SwiftUI", "Go", "Golang", "Java", "Python", "C++", "C", "VB.NET",
    "ASP.NET", "Android/Java", "iOS/Objective-C", "FastAPI", "Java Spring Boot", "Django",
    "Ruby on Rails", "PHP", "Kotlin", "Rust", "Scala", "Elixir", "Spring Boot", "Quarkus",
    " Micronaut", "Blazor", "Svelte", "SvelteKit", "Remix", "Solid.js", "Qwik", "Django", "flash", "Django Rest Framework",
    
    # === FRONTEND & STYLING (22) ===
    "Tailwind CSS", "Bootstrap", "Sass", "styled-components", "CSS Modules", "Semantic UI",
    "Lodash", "Jquery", "Apollo Client", "React-Router", "Redux", "Redux-Thunk", 
    "Redux-Saga", "Context API", "responsive design", "Framer Motion", "GSAP", "MUI",
    "Chakra UI", "Ant Design", "Material-UI", "Headless UI", "Emotion",
    
    # === DATABASES & DATA (28) ===
    "MongoDB", "MySQL", "PostgreSQL", "Redis", "DynamoDB", "NoSQL", "Oracle", "Teradata", 
    "SQL Server", "MSSQL", "MS-SQL", "DBMS", "DocumentDB", "AWS RDS", "Prisma ORM",
    "data warehousing", "Snowflake", "BigQuery", "ClickHouse", "Cassandra", "CockroachDB",
    "TimescaleDB", "PlanetScale", "Supabase", "Neon", "Firebase Firestore", "SQLite",
    
    # === CLOUD & DEVOPS/SRE (52) ===
    "AWS", "GCP", "Azure", "EC2", "Lambda", "S3", "API Gateway", "RDS", "CloudFront", 
    "Route53", "Google Cloud Platform", "Cloud Run", "Cloud Functions", "Pub/Sub", 
    "Cloud SQL", "Docker", "Kubernetes", "CI/CD", "DevOps", "Git", "GitHub", "Bitbucket",
    "Terraform", "CircleCI", "GitHub Actions", "Jenkins", "CloudWatch", "Prometheus", 
    "Grafana", "New Relic", "ELK Stack", "Site24x7", "VictorOps", "Sentry", "Pingdom", 
    "TICK stack", "Bitrise", "Xcode Cloud", "ArgoCD", "Helm", "Flux", "Pulumi", "Ansible",
    "Packer", "Consul", "Vault", "Istio", "Linkerd", "Datadog", "Honeycomb",
    
    # === QA & TESTING (38) ===
    "Selenium", "Cypress", "Playwright", "Postman", "SoapUI", "Appium", "Cucumber", 
    "Jira", "TestRail", "Zephyr", "Reqnroll", "Specflow", "xUnit", "NUnit", "MSTest",
    "manual testing", "automated testing", "test automation", "test cases", "test plans",
    "regression testing", "performance testing", "API testing", "security testing", 
    "ETL testing", "exploratory testing", "Jest", "Enzyme", "QA methodologies", "Puppeteer",
    "Vitest", "Testing Library", "Supertest", "K6", "Artillery", "Locust", "Chaos Monkey",
    
    # === DATA ENGINEERING & ML/AI (28) ===
    "SSIS", "SQL Server Integration Services", "Informatica", "DataStage", "Talend",
    "ETL testing", "LLMs", "RAGs", "NLP", "deep learning", "computer vision", 
    "GenAI", "LLM APIs", "embeddings", "vector search", "prompt workflows", "Pandas",
    "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Hugging Face", "LangChain",
    "LlamaIndex", "OpenAI API", "Pinecone", "Weaviate", "Chroma", "Kafka", "Spark",
    
    # === EMBEDDED SYSTEMS & IOT (15) ===
    "UART", "SPI", "I2C", "interrupts", "FreeRTOS", "MAVLink", "Linux", "Windows",
    "Zephyr RTOS", "NuttX", "Contiki", "Arduino", "Raspberry Pi", "ESP32", "MQTT",
    
    # === DESIGN & CREATIVE TOOLS (22) ===
    "Figma", "Adobe XD", "Sketch", "Adobe Photoshop", "Adobe Illustrator", 
    "Adobe InDesign", "Adobe Premiere Pro", "After Effects", "Canva", "CapCut",
    "CorelDRAW", "Final Cut Pro", "DaVinci Resolve", "Dreamweaver", "Blender",
    "Unity", "Unreal Engine", "Procreate", "Notion", "Miro", "Whimsical", "InVision",
    
    # === GAME DEVELOPMENT (12) ===
    "Phaser", "Three.js", "PixiJS", "Godot", "Unity", "Unreal Engine", "GameMaker",
    "Defold", "Cocos2d", "Babylon.js", "PlayCanvas", "A-Frame",
    
    # === DATA VISUALIZATION (10) ===
    "D3.js", "Chart.js", "Recharts", "Victory", "Visx", "Apache ECharts", "Plotly",
    "Highcharts", "Vega", "Observable Plot",
    
    # === BUILD TOOLS & INFRA (22) ===
    "Webpack", "Gulp", "Grunt", "Firebase", "Swagger", "OpenAPI", "Splunk",
    "TDD", "BDD", "Expo SDK", "React Native Reanimated", "React Native Skia",
    "AI-powered UI", "crypto APIs", "wallet management", "Vite", "esbuild", "RSPack",
    "Nx", "Turborepo", "Bazel",
    
    # === SECURITY & COMPLIANCE (12) ===
    "OAuth2", "JWT", "SAML", "OWASP Top 10", "Penetration Testing", "Burp Suite",
    "Metasploit", "Nmap", "Wireshark", "SSL/TLS", "PKI", "Zero Trust",
    
    # === API & INTEGRATION (10) ===
    "gRPC", "WebSockets", "Server-Sent Events", "RabbitMQ", "Redis Streams",
    "Apache ActiveMQ", "NATS", "ZMQ", "Falcor", "tRPC",
    
    # === MOBILE DEVELOPMENT (15) ===
    "SwiftUI", "Jetpack Compose", "Flutter", "React Native", "Ionic", "Capacitor",
    "NativeScript", "Xamarin", "MAUI", "Kotlin Multiplatform", "Compose Multiplatform",
    "Fastlane", "Detox", "EarlGrey", "Espresso",
    
    # === SPECIALIZED DOMAINS (18) ===
    "Web3", "blockchain", "microservices", "Elasticsearch", "data loading", 
    "data merging", "Retail data analysis", "schema design", "relational databases",
    "Serverless", "Edge Computing", "JAMstack", "Progressive Web Apps", "Headless CMS",
    "Contentful", "Strapi", "Sanity", "Directus",
    
    # === MARKETING & BUSINESS (12) ===
    "SEO", "social media marketing", "Google Ads", "Meta Ads", "copywriting",
    "graphic design", "video editing", "typography", "motion graphics", "A/B Testing",
    "Google Analytics", "Mixpanel"
    ]

    desc = description.lower()
    found_skills = set()

    for skill in skill_keywords:
        # normalize skill for matching
        pattern = re.escape(skill.lower())

        # allow spaces / hyphens interchangeably
        pattern = pattern.replace(r"\ ", r"[-\s]?")

        # enforce word boundaries
        regex = rf"\b{pattern}\b"

        if re.search(regex, desc):
            found_skills.add(skill)

    return sorted(found_skills)
