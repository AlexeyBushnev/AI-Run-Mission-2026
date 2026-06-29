# 01-stack-map

## Service
**cart-api** — checkout service

## Request path components
1. **User / client** `[mine/Product]`  
   Initiates the request and receives the response; the user-facing behavior is owned by the product/service team.

2. **Load balancer** `[ops]`  
   Accepts incoming traffic and routes requests to healthy application instances.

3. **Kubernetes cluster** `[ops]`  
   Provides the runtime floor where the containers are scheduled, scaled, and kept alive.

4. **cart-api container / service code** `[mine/Product]`  
   Executes the checkout and cart logic; this is the application behavior the product team owns.

5. **Postgres database** `[ops]`  
   Persists checkout and cart data for reads and writes.

6. **Redis cache** `[ops]`  
   Serves hot or repeated data quickly to reduce database load and latency.

7. **EPAM DIAL gateway** `[ops]`  
   Routes governed model traffic through the company gateway for the “summarise my cart” step.

8. **Language model** `[ops]`  
   Produces the AI summary response behind the gateway call.

9. **Observability stack** `[ops]`  
   Watches the whole flow with metrics, logs, traces, and AI gateway signals.

## Ownership summary
- **[mine/Product]**: user-facing app behavior, cart-api logic, acceptance bar
- **[ops]**: traffic entry, runtime floor, persistence/cache platform, AI gateway, monitoring

## Mermaid flowchart
```mermaid
flowchart LR
    U[User / Client<br/>[mine/Product]]
    LB[Load Balancer<br/>[ops]]
    K8S[Kubernetes Cluster<br/>[ops]]
    APP[cart-api Container / Service Code<br/>[mine/Product]]
    DB[(Postgres Database<br/>[ops])]
    CACHE[(Redis Cache<br/>[ops])]
    DIAL[EPAM DIAL Gateway<br/>[ops]]
    LLM[Language Model<br/>[ops]]
    OBS[Observability Stack<br/>[ops]]

    U --> LB
    LB --> K8S
    K8S --> APP

    APP --> CACHE
    CACHE --> APP

    APP --> DB
    DB --> APP

    APP --> DIAL
    DIAL --> LLM
    LLM --> DIAL
    DIAL --> APP

    APP --> K8S
    K8S --> LB
    LB --> U

    OBS -. watches .-> LB
    OBS -. watches .-> K8S
    OBS -. watches .-> APP
    OBS -. watches .-> DB
    OBS -. watches .-> CACHE
    OBS -. watches .-> DIAL
    OBS -. watches .-> LLM
```

## Check
The map includes:
- load balancer
- cluster / container runtime
- app
- database
- cache
- AI gateway
- model call
- observability
- at least one `[mine/Product]` component
