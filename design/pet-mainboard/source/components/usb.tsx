// HCTL sheet 1, recommended component-side pattern. Positive local Y is the solder row.
// The insulating alignment posts enter finished 0.80 mm plated holes tied to the shell.
export const usbLandPattern = (
  <footprint>
    {[1.75,1.25,0.75,0.25,-0.25,-0.75,-1.25,-1.75,-2.4,-3.2,2.4,3.2].map((x,i) =>
      <smtpad key={i} pcbX={x} pcbY={2.9075} width={i<8?0.3:0.6} height={1.5} shape="rect" portHints={["pin"+(i+2)]}/>)}
    {[-4.32,4.32].flatMap(x => [-3.4275,2.2925].map(y =>
      <platedhole key={x+"_"+y} pcbX={x} pcbY={y} shape="pill" holeWidth={0.60} holeHeight={1.50} outerWidth={1.0} outerHeight={1.90} portHints={["pin1"]}/>))}
    {[-3.3,3.3].map(x => <platedhole key={x} pcbX={x} pcbY={1.7225} shape="circle" holeDiameter={0.8} outerDiameter={1.12} portHints={["pin1"]}/>)}
  </footprint>
);
