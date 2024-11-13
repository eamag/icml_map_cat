<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	export let abstract: string;
	export let title: string;
	export let pdf_link: string;
</script>

<div class="card">
	<a class="card-header" href='https://openreview.net{pdf_link}'>{title}</a>
	<div class="card-content">
		Copy
<Accordion>
	<AccordionItem>
		<svelte:fragment slot="summary">(Abstract)</svelte:fragment>
		<svelte:fragment slot="content">({abstract})</svelte:fragment>
	</AccordionItem>
</Accordion>
		<p><strong>PDF:</strong> <a href=https://openreview.net/{pdf_link} target="_blank" rel="noopener noreferrer">link</a></p>
	</div>
</div>
