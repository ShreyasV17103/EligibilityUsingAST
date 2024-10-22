function visualizeTree(data) {
    const svg = d3.select("svg");
    svg.selectAll("*").remove(); // Clear previous tree

    const root = d3.hierarchy(data);
    const treeLayout = d3.tree().size([400, 300]);
    treeLayout(root);

    // Draw links between nodes
    svg.append('g')
        .selectAll('line')
        .data(root.links())
        .enter()
        .append('line')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
        .style('stroke', 'black')
        .style('stroke-width', 2);

    // Draw nodes
    svg.append('g')
        .selectAll('circle')
        .data(root.descendants())
        .enter()
        .append('circle')
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('r', 10)  // Circle radius
        .style('fill', 'steelblue');

    // Add labels to nodes
    svg.append('g')
        .selectAll('text')
        .data(root.descendants())
        .enter()
        .append('text')
        .attr('x', d => d.x + 12)  // Offset text position slightly to avoid overlap with circles
        .attr('y', d => d.y + 4)  // Center vertically
        .text(d => d.data.value)  // Display the node's value (from ASTNode)
        .style('font-size', '12px')
        .style('font-family', 'Arial');
}
