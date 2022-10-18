# blogpost & presentation

To serve the presentation:

```
jupyter nbconvert presentation.ipynb \
    --to slides \
    --post serve \
    --SlidesExporter.reveal_scroll=True \
    --TagRemovePreprocessor.remove_input_tags={\"remove-input\"}
```