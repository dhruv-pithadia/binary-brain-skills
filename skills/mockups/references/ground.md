# Ground

Learn what this project already is. Read live files, because a summary written earlier by a model is stale or wrong more often than it helps. Do not create a context file.

## Read, in this order, whatever exists

1. Identity docs: `DESIGN.md`, `PRODUCT.md`, brand or style-guide docs, README product section.
2. Tokens: Tailwind or theme config, global CSS variables, `theme.*`, design-token files, component-library theme.
3. Fonts in use and where they load from.
4. The two or three existing screens nearest to this feature: markup and styles, not just names.
5. Navigation shell where the feature will live (sidebar, tabs, header, routes).
6. Types, schema or API shape behind the feature, so mock content uses real fields.
7. UI strings on those screens, for voice (formal or casual, sentence case or title case, how errors are phrased).

## See it

If the feature touches existing UI and the app can run (use the project's dev script), run it, screenshot the nearest existing screen at 1280 and 375, and read the images. Stop only the processes you started. If it cannot run, say so and rely on the markup.

## Write down (6 to 10 lines, goes into the brief)

- **MATCH:** values and idioms the mockup must reproduce exactly: tokens, type scale, spacing rhythm, radius, elevation, component patterns, voice.
- **OPEN:** what the feature is free to decide: layout, flow, any new component.
- **IDENTITY:** how the product feels in three words, each backed by something you read.
- **STACK NOTE:** if the target is native mobile, the mock is HTML approximating platform conventions; say what fidelity that loses.

## Greenfield

No existing UI means identity is not given. Say so in the brief, take audience, domain and brand from Frame, and treat research as triggered.
