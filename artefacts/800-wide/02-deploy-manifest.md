# 02-deploy-manifest

## Input service shape
- Service: `cart-api`
- Replicas: `3`
- Memory target: `~512Mi each`
- Container port: `8080`
- Health endpoint: `/healthz`
- Required configuration: `DATABASE_URL`, `DIAL_API_KEY`

## Generated manifest (first draft)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
        - name: cart-api
          image: cart-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              value: "postgres://cart_user:password@postgres:5432/cartdb"
            - name: DIAL_API_KEY
              value: "hardcoded-api-key"
---
apiVersion: v1
kind: Service
metadata:
  name: cart-api
spec:
  selector:
    app: cart-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

## Fresh-session audit table

| Gap / missing control | Why it matters | One-line fix | Severity |
|---|---|---|---|
| No resource requests or limits | Scheduler cannot place the pod predictably and one noisy container can starve neighbors or get OOM-killed unexpectedly | Add `resources.requests` and `resources.limits`, starting around `memory: 512Mi` and appropriate CPU values | High |
| No readiness probe | During rollout, Kubernetes may send traffic to a pod before `cart-api` is actually ready, causing customer-visible errors | Add a `readinessProbe` on `GET /healthz` at port `8080` | High |
| No liveness probe | A wedged process may stay “running” forever and never self-heal | Add a `livenessProbe` on `GET /healthz` or a stricter live endpoint | Medium |
| No deployment strategy / rolling update settings | Updates can behave unpredictably and lack an explicit safe rollout posture | Add `strategy: RollingUpdate` with `maxUnavailable` / `maxSurge` values | High |
| Secrets are stored as plaintext environment values | Credentials in manifest YAML are a leakage and audit risk | Replace plaintext `env.value` with `env.valueFrom.secretKeyRef` | Critical |
| Image uses `:latest` tag | Rollbacks and reproducibility become unclear because the deployed version is not pinned | Use an immutable version or digest, e.g. `cart-api:1.2.3` or image digest | Medium |
| No rollback / revision safety settings visible | Operational recovery is slower if rollout history and revision handling are not deliberate | Set `revisionHistoryLimit` and ensure rollout history is retained | Medium |
| No explicit namespace / service account / security context | The workload may inherit unsafe defaults or run with broader permissions than needed | Add namespace, service account, and minimal `securityContext` | Medium |
| No startup probe | Slow-starting containers can be killed by liveness checks before warming up | Add `startupProbe` if the app has a meaningful startup delay | Low |
| Service exposure not tied to ingress/load balancer context | The manifest shows only an internal service and not the external traffic path from the stack map | Document or add the ingress/load-balancer layer that fronts this service | Low |

## Minimal production-oriented sketch of the fixes
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  revisionHistoryLimit: 5
  template:
    spec:
      containers:
        - name: cart-api
          image: cart-api:1.2.3
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: cart-api-secrets
                  key: DATABASE_URL
            - name: DIAL_API_KEY
              valueFrom:
                secretKeyRef:
                  name: cart-api-secrets
                  key: DIAL_API_KEY
```

## Check
The audit explicitly covers:
- resource requests / limits
- readiness / liveness
- rollback strategy
- secret handling
- replica count
- first-draft production gaps that a clean review session should catch
