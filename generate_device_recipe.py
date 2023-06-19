#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import os

import yaml

import json

import datetime

from itertools import chain

SUITABLE_FILES = [
	# Used for community ports
	"community_devices.yml",
	# Droidian official devices and generic rootfs
	"devices.yml",
]

IS_COMMUNITY_PORT = False

BUILDER_MAIN_DIRECTORY = os.path.abspath(os.path.dirname(sys.argv[0]))
BUILDER_GENERATED_DIRECTORY = os.path.join(BUILDER_MAIN_DIRECTORY, "generated")
BUILDER_OUT_DIRECTORY = os.path.join(BUILDER_MAIN_DIRECTORY, "out")

TEMPLATE = """
{{- $product := or .product "%(product)s" -}}
{{- $architecture := or .architecture "%(architecture)s" -}}
{{- $suffix := or .suffix "%(suffix)s" -}}
{{- $edition := or .edition "%(edition)s" -}}
{{- $variant := or .variant "%(variant)s" -}}
{{- $apilevel := or .apilevel %(apilevel)d -}}
{{- $version := or .version "%(version)s" -}}
{{- $mtype := or .mtype "%(mtype)s" -}}
{{- $image := or .image (printf "droidian-%%s-%%s-%%s-%%s-api%%d-%%s-%%s_%%s.zip" $mtype $edition $variant $product $apilevel $architecture $version $suffix) -}}
{{- $output_type := or .output_type "%(output_type)s" -}}
{{- $use_internal_repository := or .use_internal_repository "%(use_internal_repository)s" -}}

architecture: {{ $architecture }}
actions:

  - action: run
    description: Do nothing
    chroot: false
    command: echo "Doing nothing!"
"""

TEMPLATE_ONLY_STABLE = """
{{ if ne $version "nightly" }}
"""

TEMPLATE_ONLY_NIGHTLY = """
{{ if eq $version "nightly" }}
"""

TEMPLATE_END = """
{{end}}
"""

TEMPLATE_ENTRYPOINT = """
  - action: recipe
    description: Build Droidian
    recipe: ../rootfs-templates/device.yaml
    variables:
      architecture: {{ $architecture }}
      suffix: {{ $suffix }}
      edition: {{ $edition }}
      variant: {{ $variant }}
      apilevel: {{ $apilevel }}
      version: {{ $version }}
      image: {{ $image }}
      output_type: {{ $output_type }}
      use_internal_repository: {{ $use_internal_repository }}
"""

TEMPLATE_BUNDLE = """
  - action: recipe
    description: Generate %(name)s feature bundle
    recipe: ../rootfs-templates/recipes/sideload-create.yaml
    variables:
      architecture: %(architecture)s
      device_arch: %(architecture)s
      sideload_name: %(name)s-api%(apilevel)d-%(architecture)s_{{ $suffix }}
      packages: %(packages)s
"""

TEMPLATE_IMAGE_ADAPTATION = """
  - action: recipe
    description: Install device adaptation
    recipe: ../rootfs-templates/recipes/adaptation.yaml
    variables:
      architecture: %(architecture)s
      packages: %(packages)s
"""

def get_matrix(contents):
	"""
	Returns a JSON containing all the possible jobs.
	"""

	get_list = lambda x: x if isinstance(x, list) else [x]

	return list(
		chain(
			*[
				[
					{
						"job_name" : "%s (%s/%s edition) - %s (api%d)" % (product, edition, variant, arch, apilevel),
						"product" : product,
						"arch" : arch,
						"edition" : edition,
						"variant" : variant,
						"apilevel" : apilevel,
					}
					for arch in get_list(config.get("arch", ["arm64"]))
					for edition in get_list(config.get("edition", ["phosh"]))
					for variant in get_list(config.get("variant", ["standard"]))
					for apilevel in get_list(config.get("apilevel", [28]))
				]
				for product, config in contents.items()
				if not product.startswith(".")
			]
		)
	)

def generate_recipe_for_product(contents, product, arch, edition, variant, apilevel):
	"""
	Generates a debos recipe for the given product
	"""

	config = contents[product]

	if not os.path.exists(BUILDER_GENERATED_DIRECTORY):
		os.makedirs(BUILDER_GENERATED_DIRECTORY)

	if not os.path.exists(BUILDER_OUT_DIRECTORY):
		os.makedirs(BUILDER_OUT_DIRECTORY)

	template_config = {
		"product" : product,
		"architecture" : arch,
		"edition" : edition,
		"variant" : variant,
		"apilevel" : int(apilevel),
		"mtype" : "OFFICIAL" if not IS_COMMUNITY_PORT else "UNOFFICIAL",
		"version" : os.environ.get("DROIDIAN_VERSION", "nightly"),
		"suffix" : datetime.datetime.utcnow().strftime("%Y%m%d"),
		"output_type" : config["type"],
		"use_internal_repository" : "yes" if config.get("use_internal_repository", False) else "no",
	}

	# TODO: perhaps use pyyaml?
	with open(os.path.join(BUILDER_GENERATED_DIRECTORY, "product.yaml"), "w") as f:
		f.write(TEMPLATE % template_config)

		if config["type"] == "rootfs" and config.get("bundles", []):
			for bundle in config["bundles"]:
				write_end = False
				if bundle["arch"] in ("any", arch) and bundle.get("apilevel", 28) in ("any", int(apilevel)):
					if bundle.get("only_stable", False):
						f.write(TEMPLATE_ONLY_STABLE)
						write_end = True
					elif bundle.get("only_nightly", False):
						f.write(TEMPLATE_ONLY_NIGHTLY)
						write_end = True

					f.write(
						TEMPLATE_BUNDLE % {
							"name" : bundle["name"],
							"architecture" : arch,
							"packages" : " ".join(bundle["packages"]),
							"apilevel" : int(apilevel),
						}
					)

					if write_end:
						f.write(TEMPLATE_END)
		elif config["type"] == "rootfs" and config.get("packages", []):
			f.write(
				TEMPLATE_IMAGE_ADAPTATION % {
					"architecture" : arch,
					"packages" : " ".join(config["packages"])
				}
			)
		elif config["type"] == "image":
			f.write(
				TEMPLATE_IMAGE_ADAPTATION % {
					"architecture" : arch,
					"packages" : " ".join(config["packages"])
				}
			)

	with open(os.path.join(BUILDER_GENERATED_DIRECTORY, "droidian.yaml"), "w") as f:
		f.write(TEMPLATE % template_config)
		f.write(TEMPLATE_ENTRYPOINT)

def prompt_product(contents):
	"""
	Interactive prompt to generate_recipe_for_product().
	"""

	available = get_matrix(contents)

	print(
		"Available products:\n\n%s\n" %
		"\n".join(
			[
				"  %d) %s" % (i+1, available[i]["job_name"])
				for i in range(0, len(available))
			]
		)
	)

	choice = input("Please choose a product: ")
	try:
		choice = int(choice) - 1
		generate_recipe_for_product(
			contents,
			available[choice]["product"],
			available[choice]["arch"],
			available[choice]["edition"],
			available[choice]["variant"],
			available[choice]["apilevel"],
		)
	except:
		raise

if __name__ == "__main__":
	contents = {}

	for candidate in SUITABLE_FILES:
		path = os.path.join(BUILDER_MAIN_DIRECTORY, candidate)
		if not os.path.exists(path):
			continue

		with open(path, "r") as f:
			contents = yaml.safe_load(f)

		if candidate == "community_devices.yml":
			IS_COMMUNITY_PORT = True

		break

	argc = len(sys.argv)
	if argc == 6:
		generate_recipe_for_product(contents, *sys.argv[1:])
	elif argc == 1:
		prompt_product(contents)
	elif "--matrix" in sys.argv:
		print(json.dumps(get_matrix(contents)))
	else:
		sys.stderr.write("USAGE: generate_device_recipe.py [--matrix]|(<product_name> <arch> <edition> <variant> <apilevel>)\n")
		sys.exit(1)
