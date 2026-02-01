# src/skill_graph.py
SKILL_GRAPH = {
    # Frontend (expanded)
    "react": {
        "category": "frontend",
        "related": ["javascript", "redux", "html", "css", "nextjs", "zustand"]
    },
    "vuejs": {
        "category": "frontend",
        "related": ["javascript", "vuex", "pinia", "html", "css"]
    },
    "angular": {
        "category": "frontend",
        "related": ["typescript", "html", "css", "rxjs"]
    },
    "svelte": {
        "category": "frontend",
        "related": ["sveltekit", "javascript", "html", "css"]
    },
    "nextjs": {
        "category": "frontend",
        "related": ["react", "nodejs", "typescript"]
    },
    "nuxtjs": {
        "category": "frontend",
        "related": ["vuejs", "nodejs"]
    },
    "sveltekit": {
        "category": "frontend",
        "related": ["svelte"]
    },
    "html": {
        "category": "frontend",
        "related": ["css", "javascript"]
    },
    "css": {
        "category": "frontend",
        "related": ["html", "sass", "tailwind", "styled-components"]
    },
    "tailwind": {
        "category": "frontend",
        "related": ["css", "html", "javascript"]
    },
    "sass": {
        "category": "frontend",
        "related": ["css", "scss"]
    },
    "scss": {
        "category": "frontend",
        "related": ["sass", "css"]
    },
    "styled-components": {
        "category": "frontend",
        "related": ["react", "css"]
    },
    "typescript": {
        "category": "frontend",
        "related": ["javascript", "react", "angular", "nodejs"]
    },
    "javascript": {
        "category": "frontend",
        "related": ["react", "vuejs", "nodejs", "typescript"]
    },
    "zustand": {
        "category": "frontend",
        "related": ["react"]
    },
    "pinia": {
        "category": "frontend",
        "related": ["vuejs"]
    },
    "rxjs": {
        "category": "frontend",
        "related": ["angular"]
    },

    # Backend (expanded)
    "nodejs": {
        "category": "backend",
        "related": ["express", "nestJS", "javascript", "typescript"]
    },
    "express": {
        "category": "backend",
        "related": ["nodejs", "mongodb"]
    },
    "nestJS": {
        "category": "backend",
        "related": ["nodejs", "typescript", "typeorm"]
    },
    "python": {
        "category": "backend",
        "related": ["django", "flask", "fastapi", "celery"]
    },
    "django": {
        "category": "backend",
        "related": ["python", "djangorestframework"]
    },
    "flask": {
        "category": "backend",
        "related": ["python"]
    },
    "fastapi": {
        "category": "backend",
        "related": ["python", "pydantic"]
    },
    "java": {
        "category": "backend",
        "related": ["springboot", "hibernate", "maven"]
    },
    "springboot": {
        "category": "backend",
        "related": ["java", "spring-security"]
    },
    "go": {
        "category": "backend",
        "related": ["gin", "echo", "gorm"]
    },
    "gin": {
        "category": "backend",
        "related": ["go"]
    },
    "echo": {
        "category": "backend",
        "related": ["go"]
    },
    "rust": {
        "category": "backend",
        "related": ["actix-web", "rocket"]
    },
    "actix-web": {
        "category": "backend",
        "related": ["rust"]
    },
    "php": {
        "category": "backend",
        "related": ["laravel", "symfony"]
    },
    "laravel": {
        "category": "backend",
        "related": ["php"]
    },
    "ruby": {
        "category": "backend",
        "related": ["rails"]
    },
    "rails": {
        "category": "backend",
        "related": ["ruby"]
    },
    "djangorestframework": {
        "category": "backend",
        "related": ["django"]
    },
    "pydantic": {
        "category": "backend",
        "related": ["fastapi", "python"]
    },
    "spring-security": {
        "category": "backend",
        "related": ["springboot"]
    },

    # Databases (expanded)
    "mongodb": {
        "category": "database",
        "related": ["mongoose", "nosql"]
    },
    "postgresql": {
        "category": "database",
        "related": ["sql", "prisma", "typeorm"]
    },
    "mysql": {
        "category": "database",
        "related": ["sql"]
    },
    "redis": {
        "category": "database",
        "related": ["caching", "pubsub"]
    },
    "sqlite": {
        "category": "database",
        "related": ["sql"]
    },
    "elasticsearch": {
        "category": "database",
        "related": ["search"]
    },
    "prisma": {
        "category": "database",
        "related": ["postgresql", "mysql"]
    },
    "mongoose": {
        "category": "database",
        "related": ["mongodb"]
    },
    "typeorm": {
        "category": "database",
        "related": ["postgresql", "nestJS"]
    },
    "gorm": {
        "category": "database",
        "related": ["go"]
    },

    # DevOps & Cloud (expanded)
    "docker": {
        "category": "devops",
        "related": ["kubernetes", "docker-compose"]
    },
    "kubernetes": {
        "category": "devops",
        "related": ["docker", "helm", "k8s"]
    },
    "docker-compose": {
        "category": "devops",
        "related": ["docker"]
    },
    "helm": {
        "category": "devops",
        "related": ["kubernetes"]
    },
    "aws": {
        "category": "cloud",
        "related": ["lambda", "ec2", "s3", "eks"]
    },
    "azure": {
        "category": "cloud",
        "related": ["azure-devops", "aks"]
    },
    "gcp": {
        "category": "cloud",
        "related": ["cloud-run", "gke"]
    },
    "terraform": {
        "category": "devops",
        "related": ["infrastructure", "iac"]
    },
    "ansible": {
        "category": "devops",
        "related": ["configuration"]
    },
    "jenkins": {
        "category": "devops",
        "related": ["cicd"]
    },
    "github-actions": {
        "category": "devops",
        "related": ["cicd", "git"]
    },

    # Tools & Testing
    "git": {
        "category": "tools",
        "related": ["github", "gitlab"]
    },
    "github": {
        "category": "tools",
        "related": ["git"]
    },
    "gitlab": {
        "category": "tools",
        "related": ["git"]
    },
    "postman": {
        "category": "tools",
        "related": ["api-testing"]
    },
    "jest": {
        "category": "testing",
        "related": ["javascript", "react"]
    },
    "pytest": {
        "category": "testing",
        "related": ["python"]
    },
    "junit": {
        "category": "testing",
        "related": ["java"]
    },

    # AI/ML & Data (expanded)
    "tensorflow": {
        "category": "ai",
        "related": ["python", "keras"]
    },
    "pytorch": {
        "category": "ai",
        "related": ["python", "torch"]
    },
    "keras": {
        "category": "ai",
        "related": ["tensorflow", "python"]
    },
    "scikit-learn": {
        "category": "ai",
        "related": ["python", "pandas"]
    },
    "pandas": {
        "category": "data",
        "related": ["python", "numpy"]
    },
    "numpy": {
        "category": "data",
        "related": ["python"]
    },
    "celery": {
        "category": "backend",
        "related": ["python", "redis"]
    },

    # State Management
    "redux": {
        "category": "frontend",
        "related": ["react"]
    },
    "vuex": {
        "category": "frontend",
        "related": ["vuejs"]
    },
    "maven": {
        "category": "build",
        "related": ["java"]
    }
}


CATEGORY_ALIASES = {
    "frontend": [
        "react", "vuejs", "angular", "svelte", "nextjs", "nuxtjs", "sveltekit",
        "html", "css", "javascript", "typescript", "tailwind", "sass", "scss",
        "styled-components", "zustand", "pinia", "redux", "vuex", "rxjs"
    ],
    "backend": [
        "nodejs", "express", "nestJS", "python", "django", "flask", "fastapi",
        "djangorestframework", "java", "springboot", "spring-security",
        "go", "gin", "echo", "rust", "actix-web", "php", "laravel",
        "ruby", "rails", "pydantic", "celery"
    ],
    "database": [
        "mongodb", "postgresql", "mysql", "redis", "sqlite", "elasticsearch",
        "sql", "nosql", "prisma", "mongoose", "typeorm", "gorm"
    ],
    "devops": [
        "docker", "kubernetes", "docker-compose", "helm", "terraform", "ansible",
        "jenkins", "github-actions", "cicd", "k8s"
    ],
    "cloud": [
        "aws", "azure", "gcp", "lambda", "ec2", "s3", "eks", "azure-devops",
        "aks", "cloud-run", "gke"
    ],
    "tools": [
        "git", "github", "gitlab", "postman", "jwt", "maven"
    ],
    "testing": [
        "jest", "pytest", "junit", "api-testing", "authentication"
    ],
    "ai": [
        "tensorflow", "pytorch", "keras", "scikit-learn"
    ],
    "data": [
        "pandas", "numpy"
    ],
    "build": [
        "infrastructure", "iac", "configuration"
    ]
}

