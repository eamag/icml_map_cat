<script lang="ts">
	export let title: string;
	export let classification_reasoning: string;
	export let problems_addressed: string;
	export let follow_up_tasks: string;
	export let further_research: string; // Now a string
	export let outstanding_paper_award_probability: number;
	export let startup_based_on_paper: string;
	export let alternative_classifications: string;
	export let pdf_link: string;

	// Parse JSON strings into arrays or objects
	let problemsAddressedList: string[] = [];
	let followUpTasksList: { difficulty: number; task: string }[] = [];
	let alternativeClassificationsList: { field: string; discipline: string; sub_discipline: string; area: string; topic: string; subtopic: string }[] = [];

	try {
		problemsAddressedList = JSON.parse(problems_addressed);
	} catch (e) {
		console.error('Error parsing problems_addressed JSON:', e);
	}

	try {
		followUpTasksList = JSON.parse(follow_up_tasks);
	} catch (e) {
		console.error('Error parsing follow_up_tasks JSON:', e);
	}

	try {
		alternativeClassificationsList = JSON.parse(alternative_classifications);
	} catch (e) {
		console.error('Error parsing alternative_classifications JSON:', e);
	}
</script>

<div class="card p-4">
	<div class="card-header">{title}</div>
	<div class="card-content">
		<p><strong>PDF:</strong> <a href={pdf_link} target="_blank" rel="noopener noreferrer">link</a></p>
		<p><strong>Classification Reasoning:</strong> {classification_reasoning}</p>
		<p><strong>Problems Addressed:</strong></p>
		<ol class="list">
			{#each problemsAddressedList as problem, index}
				<li>
					<span>{index + 1}.</span>
					<span class="flex-auto">{problem}</span>
				</li>
			{/each}
		</ol>
		<p><strong>Follow-Up Tasks:</strong></p>
		<ol class="list">
			{#each followUpTasksList as task, index}
				<li>
					<span>{index + 1}.</span>
					<span class="flex-auto">Difficulty {task.difficulty}: {task.task}</span>
				</li>
			{/each}
		</ol>
		<p><strong>Further Research:</strong> {further_research}</p>
		<p><strong>Outstanding Paper Award Probability:</strong> {outstanding_paper_award_probability * 100}%</p>
		<p><strong>Startup Based on Paper:</strong> {startup_based_on_paper}</p>
		<p><strong>Alternative Classifications:</strong></p>
		<ul class="list">
			{#each alternativeClassificationsList as classification, index}
				<li>
					<span>{index + 1}.</span>
					<span class="flex-auto">{classification.field} - {classification.discipline} - {classification.sub_discipline} - {classification.area} - {classification.topic} - {classification.subtopic}</span>
				</li>
			{/each}
		</ul>
	</div>
</div>
