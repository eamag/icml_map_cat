<script lang="ts">
	import { RecursiveTreeView, type TreeViewNode } from '@skeletonlabs/skeleton';
	import PaperCard from '$lib/PaperCard.svelte';

	interface Paper {
		id: string;
		classification_reasoning: string;
		problem: string;
		further_research: string;
		outstanding_paper_award_probability: number;
		pdf_link: string;
		title: string;
	}

	const convertToTreeViewNodes = (data: any): TreeViewNode[] => {
		const treeViewNodes: TreeViewNode[] = [];

		const buildTree = (nodeData: any): TreeViewNode[] => {
			return Object.keys(nodeData).map((key) => {
				const node: TreeViewNode = {
					id: key,
					content: key,
					children: Array.isArray(nodeData[key])
						? nodeData[key].map((paper: Paper) => ({
								id: paper.id,
								content: PaperCard,
								contentProps: paper
							}))
						: buildTree(nodeData[key])
				};
				return node;
			});
		};

		treeViewNodes.push(...buildTree(data));

		return treeViewNodes;
	};

	// export let data: any;
	import papers from '$lib/data.json';
	const myTreeViewNodes: TreeViewNode[] = convertToTreeViewNodes(papers);
</script>

<h3 class="h3 text-center">
	I classify ICLR 2024 papers into different categories. On this page I predict 4 categories and sub
	category levels at the same time using Cohere R+
</h3>
<RecursiveTreeView nodes={myTreeViewNodes} />
