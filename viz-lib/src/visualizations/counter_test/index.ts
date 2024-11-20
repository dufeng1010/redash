import Renderer from "./Renderer";
import Editor from './Editor'



const DEFAULT_OPTIONS = {
    counterLabel: "",
    counterColName: "yandufeng",
    rowNumber: 1,
    targetRowNumber: 200,
    stringDecimal: 100,
    stringDecChar: ".",
    stringThouSep: ",",
    tooltipFormat: "0,0.000",
}

export default {
    Type: "Yandufeng",
    name: "yandufeng",
    getOptions: (options: any) => ({
        ...DEFAULT_OPTIONS,
        ...options,
    }),
    Renderer,
    Editor,

    defaultColumns: 2,
    defaultRows: 5,
}