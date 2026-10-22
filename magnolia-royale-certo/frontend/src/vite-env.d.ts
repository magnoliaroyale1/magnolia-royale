/// <reference types="vite/client" />
/// <reference types="react" />
/// <reference types="react-dom" />

declare module '*.css' {
    const content: { [className: string]: string }
    export default content
  }
  
  declare module '*.svg' {
    const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>
    export default content
  }