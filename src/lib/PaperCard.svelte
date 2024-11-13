<!-- PaperCard.svelte -->
<script lang="ts">
	export let id: string;
	export let classification_reasoning: string;
	export let problem: string;
	export let further_research: string;
	export let outstanding_paper_award_probability: number;
	export let pdf_link: string;
	export let title: string;

	// Parse further_research JSON string into an array
	let furtherResearchList: string[] = [];
	try {
		furtherResearchList = JSON.parse(further_research);
	} catch (e) {
		console.error('Error parsing further_research JSON:', e);
	}
</script>

<div class="card p-4">
	<div class="card-header">{title}</div>
	<div class="card-content">
		<p>OpenReview ID: {id}</p>
		<p>Problem: {problem}</p>
		<p>Classification Reasoning: {classification_reasoning}</p>
		<p>Further Research:</p>
		<ol class="list">
			{#each furtherResearchList as researchItem, index}
				<li>
					<span>{index + 1}.</span>
					<span class="flex-auto">{researchItem}</span>
				</li>
			{/each}
		</ol>
		<p>Outstanding Paper Award Probability: {outstanding_paper_award_probability * 100}%</p>
		<p>PDF: <a href={pdf_link} target="_blank" rel="noopener noreferrer">link</a></p>
	</div>
</div>