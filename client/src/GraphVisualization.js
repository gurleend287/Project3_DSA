import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const GraphVisualization = ({ graphData }) => {
  const ref = useRef(null);

  useEffect(() => {
    if (graphData) {
      const svg = d3.select(ref.current);

      // Clear previous graph
      svg.selectAll('*').remove();

      // Create nodes
      const nodes = svg.selectAll('.node')
        .data(graphData.nodes)
        .enter()
        .append('circle')
        .attr('class', 'node')
        .attr('r', 10)
        .attr('fill', 'blue');

      // Create links
      const links = svg.selectAll('.link')
        .data(graphData.links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('stroke-width', 2)
        .attr('stroke', 'gray');

      // Simulation
      const simulation = d3.forceSimulation(graphData.nodes)
        .force('link', d3.forceLink(graphData.links).id(d => d.id))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(400, 400));

      // Update node and link positions
      simulation.on('tick', () => {
        nodes.attr('cx', d => d.x)
          .attr('cy', d => d.y);

        links.attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);
      });
    }
  }, [graphData]);

  return (
    <svg ref={ref} width="800" height="800"></svg>
  );
};

export default GraphVisualization;
