# 03-ci-workflow

## Pipeline ask
Build, test, security-scan, and deploy `cart-api` as a container image on every push to `main`.

Deploy target context:
- Kubernetes deployment for `cart-api`
- Containerized service behind the manifest from Kata 8.2

## Generated workflow (first draft)

```yaml
name: cart-api-ci-cd

on:
  push:
    branches: [main]

jobs:
  build-test-scan-deploy:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Dependency scan
        run: npm audit --audit-level=high

      - name: Build image
        run: docker build -t my-registry/cart-api:${{ github.sha }} .

      - name: Log in to registry
        run: echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login my-registry -u "${{ secrets.REGISTRY_USER }}" --password-stdin

      - name: Push image
        run: docker push my-registry/cart-api:${{ github.sha }}

      - name: Deploy
        run: kubectl apply -f k8s/cart-api.yaml
```

## Fresh-session audit — six supply-chain controls

| Control | Status | Why it matters | One-line fix |
|---|---|---|---|
| Pinned action versions | **Partial** | `@v4` is only a tag, not an immutable pin; a moved tag can change what runs in CI | Pin third-party actions to a full commit SHA instead of a floating major tag |
| OIDC short-lived credentials instead of long-lived secrets | **Missing** | Long-lived registry credentials in secrets are a high-value target and hard to rotate safely | Replace registry username/password secrets with OIDC-based short-lived workload identity |
| Image signing / provenance | **Missing** | Without signing and provenance, downstream systems cannot verify that the image came from this pipeline | Add image signing and provenance generation, e.g. cosign + SLSA-style attestations |
| Dependency + image scanning | **Partial** | The workflow has `npm audit`, but no container image scan; supply-chain risk lives in both dependencies and built images | Keep dependency scanning and add image scanning before deploy |
| Least-privilege token scope | **Partial** | `contents: read` is good, but deploy and signing steps often need narrowly scoped explicit permissions, not defaults or broad tokens | Declare only the exact permissions needed for checkout, OIDC, packages, attestations, and deployment |
| Rollback gate | **Missing** | A bad deployment with no rollback gate turns a failed rollout into a longer incident | Add a post-deploy verification step and an explicit rollback gate / rollback command path |

## Expected first-draft misses
The first-draft workflow misses or weakly handles the controls it most often misses:
1. unpinned third-party actions (`@v4` tags)
2. long-lived registry password in a stored secret
3. no image signing / provenance
4. no rollback gate

## Example tightened direction
```yaml
permissions:
  contents: read
  id-token: write
  packages: write

# Then:
# - pin actions to commit SHAs
# - use OIDC for registry/cloud auth
# - run dependency + image scan
# - sign the image and emit provenance
# - deploy only after checks pass
# - add a post-deploy verification + rollback path
```

## Check
This audit explicitly covers:
- pinned action versions
- OIDC short-lived credentials vs long-lived secrets
- image signing / provenance
- dependency and image scanning
- least-privilege token permissions
- rollback gate
