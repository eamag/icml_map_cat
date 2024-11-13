<script lang="ts">
	import 'leaflet/dist/leaflet.css';
	import 'leaflet.markercluster/dist/MarkerCluster.css';
	import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { autoModeWatcher } from '@skeletonlabs/skeleton';
	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('javascript', javascript);
	hljs.registerLanguage('typescript', typescript);
	storeHighlightJs.set(hljs);

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<svelte:head>
	{@html '<script>(' + autoModeWatcher.toString() + ')();</script>'}
	<title>AI conference paper analysis 2024</title>
	<meta
		name="description"
		content="Explore an interactive world map of institutions publishing at ICML 2024. Discover global
	AI research hotspots and gain insights into the geographical distribution of machine learning contributions."
	/>
</svelte:head>
<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<a class="lg:!ml-0 w-[32px] lg:w-auto" href="/" title="Go to Homepage">
					<strong class="text-xl uppercase">Map</strong>
				</a>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<div class="flex-none">
					<a class="btn btn-sm variant-ghost-surface" href="https://eamag.me/2024/ICML-2024-on-a-map" target="_blank">About ICML map</a>
					<a
						class="btn btn-sm variant-ghost-surface"
						target="_blank"
						href="https://eamag.me/2024/Automated-Paper-Classification"
					>
						About classifications
					</a>
					<a class="btn btn-sm variant-ghost-surface" href="/datatable">ICML table</a>
					<a class="btn btn-sm variant-ghost-surface" href="/iclr">ICLR</a>
					<a class="btn btn-sm variant-ghost-surface" href="/icml_gemini_flash">
						ICML 2024 Gemini Flash topics
					</a>
					<a class="btn btn-sm variant-ghost-surface" href="/icml_embeddings">
						ICML topics embeddings
					</a>
					<a
						class="btn btn-sm variant-ghost-surface"
						href="https://twitter.com/EamagAI"
						target="_blank"
					>
						X/Twitter
					</a>
				</div>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>
