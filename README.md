<p align="center">
  <img src="assets/community-banner.svg" alt="sparkrun — Community Recipe Registry" width="560" />
</p>

<p align="center">
  <a href="https://github.com/spark-arena/sparkrun"><img src="https://img.shields.io/badge/sparkrun-CLI-1e40af" alt="sparkrun CLI" /></a>
  <a href="https://sparkrun.dev"><img src="https://img.shields.io/badge/docs-sparkrun.dev-1e40af" alt="Documentation" /></a>
  <a href="https://spark-arena.com"><img src="https://img.shields.io/badge/Spark_Arena-community-76b900" alt="Spark Arena" /></a>

[//]: # (  <a href="https://recipes.sparkrun.dev"><img src="https://img.shields.io/badge/browse-recipes-76b900" alt="Browse Recipes" /></a>)
</p>

<h3 align="center">Community-contributed inference recipes for NVIDIA DGX Spark</h3>

<p align="center">
  Share your optimized model configs, discover what others are running, and benchmark on <a href="https://spark-arena.com">Spark Arena</a>.
</p>

---

This is the **community recipe registry** for [sparkrun](https://github.com/spark-arena/sparkrun). Anyone can submit a
recipe via pull request and make it available to every sparkrun user.

Community recipes are run with the `@community` prefix:

```bash
sparkrun run @community/awesome-recipe-username
```

## Directory Structure Guidance

You should follow the following directory structure:

recipes/{model}/{user}/{model}-{quant}-{mtp}-{runtime}-{user}.yaml

* You can add a README.md and supporting files under recipes/{model}/{user}; however, note that
  only the recipe yaml file will be considered part of the recipe.
* The model name should come first for tab completion at the command line.
* The recipe filename is the canonical lookup for the recipe, so it cannot overlap with other recipes and should provide
  sufficient data to understand the key inputs.
* If quantization is not applicable, still provide the native dtype (e.g. bf16 for bfloat16, fp8, etc.) for clarity. (re: {quant})
* If MTP/dflash/etc. not applicable, then leave it out. (re: {mtp})
* All community recipes should include your username at the end of the recipe filename for differentiation.

NOTE: Integration with Spark Arena Benchmarks coming soon!

## Submit a Recipe

1. **Fork** this repository
2. **Create** your recipe YAML in `recipes/`:
   ```
   recipes/
     model-name/
       user-name/
         {model}-{quant}-{mtp}-{runtime}-{user}.yaml
   ```
3. **Open a pull request** — describe what the recipe runs, which runtime it targets, and expected VRAM usage
4. Once merged, your recipe is live for everyone

### Recipe format

Recipes follow the standard sparkrun recipe schema. See
the [recipe authoring docs](https://sparkrun.dev/recipes/overview/) for the full specification.

## Run Community Recipes

```bash
# List available community recipes
sparkrun list @community

# Run a community recipe
sparkrun run @community/my-awesome-recipe

# Check VRAM requirements before launching
sparkrun show @community/my-awesome-recipe
```

## Benchmark Your Recipes

Got a recipe that screams? Prove it.

Submit your recipe benchmark to [Spark Arena](https://spark-arena.com) to benchmark your recipes and see how they stack
up. Publish your numbers and show the community what DGX Spark can do.

```
# Login to Spark Arena (if not already logged in) -- see https://spark-arena.com for details
sparkrun arena login

# Benchmark your recipes (this will run the recipe, benchmark it, stop it, and upload the result to Spark Arena in one step)
sparkrun arena benchmark @community/my-awesome-recipe
```

Then you can go to https://spark-arena.com/leaderboard to see how you stack up!

## Links

- [sparkrun](https://github.com/spark-arena/sparkrun) — the tool that runs recipes
- [sparkrun docs](https://sparkrun.dev) — full documentation
- [Spark Arena](https://spark-arena.com) — community hub and benchmarking

[//]: # (- [Recipe Explorer]&#40;https://recipes.sparkrun.dev&#41; — browse and filter all recipes)

