<script lang="ts">
	import { RecursiveTreeView, type TreeViewNode } from '@skeletonlabs/skeleton';
	import PaperCard from '$lib/PaperCardICML.svelte';

	interface Paper {
		id: string;
		title: string;
		classification_reasoning: string;
		field: string;
		discipline: string;
		sub_discipline: string;
		area: string;
		topic: string;
		subtopic: string;
		problems_addressed: string;
		follow_up_tasks: string;
		further_research: string;
		outstanding_paper_award_probability: number;
		startup_based_on_paper: string;
		alternative_classifications: string;
		pdf_link: string;
	}

	const convertToTreeViewNodes = (data: any): TreeViewNode[] => {
		const treeViewNodes: TreeViewNode[] = [];

		const buildTree = (nodeData: any, nodeId: string = ''): TreeViewNode[] => {
			return Object.keys(nodeData).map((key) => {
				const id = nodeId ? `${nodeId}-${key}` : key;
				if (Array.isArray(nodeData[key])) {
					return {
						id: id,
						content: key,
						children: nodeData[key].map((paper: Paper) => ({
							id: paper.id,
							content: PaperCard,
							contentProps: { ...paper }
						}))
					};
				} else {
					return {
						id: id,
						content: key,
						children: buildTree(nodeData[key], id)
					};
				}
			});
		};

		treeViewNodes.push(...buildTree(data));

		return treeViewNodes;
	};

	import nestedData from '$lib/nested_data.json';
	const myTreeViewNodes: TreeViewNode[] = convertToTreeViewNodes(nestedData);
</script>

<h3 class="h3 text-center">
	I classify ICML 2024 papers into different categories. On this page I predict one category at a
	time and adjust a prompt to have a choice from sub categories using Gemini Flash
</h3>
<RecursiveTreeView nodes={myTreeViewNodes} />
