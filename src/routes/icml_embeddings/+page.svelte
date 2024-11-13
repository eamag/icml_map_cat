<script lang="ts">
	import { RecursiveTreeView, type TreeViewNode } from '@skeletonlabs/skeleton';
	import PaperCard from './PaperCardICML.svelte';

	interface Paper {
		id: string;
		title: string;
		abstract: string;
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

	import nestedData from '$lib/embed_data.json';
	const myTreeViewNodes: TreeViewNode[] = convertToTreeViewNodes(nestedData);
</script>

<h3 class="h3 text-center">
	I classify ICML 2024 papers into different categories. On this page I created embeddings for each
	paper using Qwen 2 and clustered them together using HDBSCAN recursively, then labeled these clusters
	automatically.
</h3>
<RecursiveTreeView nodes={myTreeViewNodes} />
