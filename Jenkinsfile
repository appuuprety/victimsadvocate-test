// Jenkins declarative pipeline for VictimsAdvocate end-to-end tests.
//
// Required Jenkins credentials (Manage Jenkins → Credentials):
//   - va-supabase-url        (Secret text)
//   - va-supabase-anon-key   (Secret text)
//   - va-admin-email         (Secret text)
//   - va-admin-password      (Secret text)
//
// Required agent tools:
//   - Python 3.11+
//   - Node.js 20+
//   - git
//
// Triggered on every push (configure as a Multibranch Pipeline against
// https://github.com/appuuprety/victimsadvocate-test).

pipeline {
  agent any

  options {
    timeout(time: 20, unit: 'MINUTES')
    timestamps()
    ansiColor('xterm')
  }

  environment {
    APP_REPO       = 'https://github.com/appuuprety/victimsadvocate.git'
    APP_BRANCH     = 'main'
    BASE_URL       = 'http://localhost:5173'
    PIP_NO_INPUT   = '1'
  }

  stages {
    stage('Checkout tests') {
      steps {
        checkout scm
      }
    }

    stage('Checkout app') {
      steps {
        dir('app') {
          git branch: env.APP_BRANCH, url: env.APP_REPO
        }
      }
    }

    stage('Install Python deps') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --quiet --upgrade pip
          pip install --quiet -r requirements.txt
          playwright install --with-deps chromium
        '''
      }
    }

    stage('Build & start app') {
      steps {
        withCredentials([
          string(credentialsId: 'va-supabase-url',      variable: 'VITE_SUPABASE_URL'),
          string(credentialsId: 'va-supabase-anon-key', variable: 'VITE_SUPABASE_ANON_KEY'),
        ]) {
          dir('app') {
            sh '''
              echo "VITE_SUPABASE_URL=$VITE_SUPABASE_URL" > .env
              echo "VITE_SUPABASE_ANON_KEY=$VITE_SUPABASE_ANON_KEY" >> .env
              npm ci
              npm run build
              # Serve the production build in the background
              nohup npx vite preview --port 5173 --host 0.0.0.0 > ../vite.log 2>&1 &
              echo $! > ../vite.pid
            '''
          }
          // Wait for the server to come up
          sh '''
            for i in $(seq 1 30); do
              if curl -fs http://localhost:5173 >/dev/null; then
                echo "App is up"; exit 0
              fi
              sleep 1
            done
            echo "App failed to start"; cat vite.log; exit 1
          '''
        }
      }
    }

    stage('Run tests') {
      steps {
        withCredentials([
          string(credentialsId: 'va-supabase-url',      variable: 'SUPABASE_URL'),
          string(credentialsId: 'va-supabase-anon-key', variable: 'SUPABASE_ANON_KEY'),
          string(credentialsId: 'va-admin-email',       variable: 'ADMIN_EMAIL'),
          string(credentialsId: 'va-admin-password',    variable: 'ADMIN_PASSWORD'),
        ]) {
          sh '''
            . .venv/bin/activate
            pytest \
              --junitxml=test-results/junit.xml \
              --tracing=retain-on-failure \
              --output=test-results
          '''
        }
      }
    }
  }

  post {
    always {
      // Stop the preview server
      sh '''
        if [ -f vite.pid ]; then
          kill $(cat vite.pid) || true
          rm -f vite.pid
        fi
      '''
      junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
      archiveArtifacts artifacts: 'test-results/**, vite.log', allowEmptyArchive: true
    }
    failure {
      echo 'Tests failed — see archived traces in test-results/'
    }
  }
}
