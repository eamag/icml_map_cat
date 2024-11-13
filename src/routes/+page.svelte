<script lang="ts">
	import { onMount } from 'svelte';
	import type { Map, Marker } from 'leaflet';
	import data from '$lib/markers.json';

	let map: Map;
	let markers: any;
	let paperList: { institution: string; papers: string[] } | null = null;

	interface InstitutionInfo {
		location: [number, number];
		address: string | null;
		papers: string[];
		original_names: string[];
	}

	type Data = {
		[institution: string]: InstitutionInfo;
	};

	onMount(async () => {
		const L = await import('leaflet');
		const { MarkerClusterGroup }: any = await import('leaflet.markercluster');

		// Initialize the map
		map = L.map('map').setView([48.1174917, -1.6382906], 3);

		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; OpenStreetMap contributors'
		}).addTo(map);
		var greenIcon = L.icon({
			iconUrl: 'lab.jpg',
			iconSize: [30, 30], // size of the icon
		});
		markers = new MarkerClusterGroup();

		const processedData: Data = data as unknown as Data;

		Object.entries(processedData).forEach(([institution, info]) => {
			if (info.location == null || info.location.length !== 2) {
				console.error(`Invalid location for ${institution} ${JSON.stringify(info.location)}`);
				return;
			}
			const marker: Marker = L.marker(info.location as [number, number], {icon: greenIcon});
			const paperLinks = info.papers
				.map(
					(paper) =>
						`<a href="https://openreview.net/forum?id=${paper}" target="_blank">${paper}</a>`
				)
				.join('<br>');

			marker.bindPopup(`<b>${institution}</b><br>Papers:<br>${paperLinks}`);
			markers.addLayer(marker);

			marker.on('click', () => {
				paperList = { institution, papers: info.papers };
			});
		});

		map.addLayer(markers);
		map.fitBounds(markers.getBounds());
	});
</script>

<hr class="border-t-2" />
<div class="card p-4">
	<header class="h2 text-center p-1">ICML 2024 Institutions and Associated Papers</header>
	<section class="text-center">
		I wanted to know what research in AI is published by people around my area. So I got all papers
		from the 2024 International Conference on Machine Learning from openreview.net, extracted all
		authors and their affiliations using gemma-2, used nominatim, google maps and search with
		gemma-2 on top to find addresses and put them on the map. Expect to see some errors, contact me
		on X/Twitter and I can manually fix them :) Details are in <a class="anchor" href="https://eamag.me/2024/ICML-2024-on-a-map" target="_blank"> this blog post</a>.
	</section>
</div>
<hr class="border-t-1" />
<div id="map" class="h-4/5 rounded p-1"></div>
<hr class="border-t-1" />
<ul class="list text-center p-1">
	{#if paperList}
		<h2>Links to papers from {paperList.institution}</h2>
		{#each paperList.papers as paper}
			<li class="justify-center">
				<span
					><a class="anchor" href="https://openreview.net/forum?id={paper}" target="_blank"
						>Paper ID: {paper}</a
					></span
				>
			</li>
		{/each}
	{:else}
		<p class="text-center">Click on a marker to see papers.</p>
	{/if}
</ul>
