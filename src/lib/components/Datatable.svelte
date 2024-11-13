<script>
	import ThSort from '$lib/components/client/ThSort.svelte';
	import ThFilter from '$lib/components/client/ThFilter.svelte';
	import Search from '$lib/components/client/Search.svelte';
	import RowCount from '$lib/components/client/RowCount.svelte';
	import Pagination from '$lib/components/client/Pagination.svelte';

	import data from '$lib/data.js';

	import { DataHandler } from '@vincjo/datatables';

	//Init data handler - CLIENT
	const handler = new DataHandler(data.papers, { rowsPerPage: 5 });
	const rows = handler.getRows();
</script>

<div class="table-container space-y-4">
	<header class="flex justify-between gap-4">
		<Search {handler} />
	</header>
	<table class="table table-hover table-compact table-auto w-full">
		<thead>
			<tr>
				<ThSort {handler} orderBy="title">Title</ThSort>
				<ThSort {handler} orderBy="classification_reasoning">Classification Reasoning</ThSort>
				<ThSort {handler} orderBy="sub_discipline">Sub Discipline</ThSort>
				<ThSort {handler} orderBy="area">Area</ThSort>
				<ThSort {handler} orderBy="topic">Topic</ThSort>
				<ThSort {handler} orderBy="subtopic">Subtopic</ThSort>
				<ThSort {handler} orderBy="problems_addressed">Problems Addressed</ThSort>
				<ThSort {handler} orderBy="follow_up_tasks">Follow Up Tasks</ThSort>
				<ThSort {handler} orderBy="further_research">Further Research</ThSort>
				<ThSort {handler} orderBy="outstanding_paper_award_probability">Outstanding Paper Award Probability</ThSort>
				<ThSort {handler} orderBy="startup_based_on_paper">Startup Based On Paper</ThSort>
				<ThSort {handler} orderBy="alternative_classifications">Alternative Classifications</ThSort>
				<ThSort {handler} orderBy="pdf_link">PDF Link</ThSort>
			</tr>
			<tr>
				<ThFilter {handler} filterBy="title" />
				<ThFilter {handler} filterBy="classification_reasoning" />
				<ThFilter {handler} filterBy="sub_discipline" />
				<ThFilter {handler} filterBy="area" />
				<ThFilter {handler} filterBy="topic" />
				<ThFilter {handler} filterBy="subtopic" />
				<ThFilter {handler} filterBy="problems_addressed" />
				<ThFilter {handler} filterBy="follow_up_tasks" />
				<ThFilter {handler} filterBy="further_research" />
				<ThFilter {handler} filterBy="outstanding_paper_award_probability" />
				<ThFilter {handler} filterBy="startup_based_on_paper" />
				<ThFilter {handler} filterBy="alternative_classifications" />
				<ThFilter {handler} filterBy="pdf_link" />
			</tr>
		</thead>
		
		<tbody>
			{#each $rows as row}
				<tr>
					<td>{row.title}</td>
					<td>{row.classification_reasoning}</td>
					<td>{row.sub_discipline}</td>
					<td>{row.area}</td>
					<td>{row.topic}</td>
					<td>{row.subtopic}</td>
					<td>
						<ul>
							{#each row.problems_addressed as problem}
								<li>{problem}</li>
							{/each}
						</ul>
					</td>
					<td>
						<ol class="list">
							{#each row.follow_up_tasks as task}
								<li>
									<span>Difficulty level {task.difficulty} </span>
									<span class="flex-auto"> {task.task}</span> 
								</li>
							{/each}
						</ol>
					</td>
					<td>{row.further_research}</td>
					<td>{row.outstanding_paper_award_probability}</td>
					<td>{row.startup_based_on_paper}</td>
					<td>
						<ul>
							{#each row.alternative_classifications as alt}
								<li>
									Field: {alt.field}, Discipline: {alt.discipline}, Topic: {alt.topic}, Subtopic: {alt.subtopic},
									Sub-discipline: {alt.sub_discipline}, Area: {alt.area}
								</li>
							{/each}
						</ul>
					</td>
					<td><a href={row.pdf_link}>PDF Link</a></td>
				</tr>
			{/each}
		</tbody>
	</table>
	<!-- Footer -->
	<footer class="flex justify-between">
		<RowCount {handler} />
		<Pagination {handler} />
	</footer>
</div>
