
# Minimal Makefile for Sphinx documentation
#
# You can invoke this from the repo root with:
#   make -C docs html

SPHINXBUILD   ?= sphinx-build
SPHINXOPTS    ?=
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html dirhtml latexpdf

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	@rm -rf "$(BUILDDIR)"

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

dirhtml:
	@$(SPHINXBUILD) -M dirhtml "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

latexpdf:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
