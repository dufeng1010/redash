import { map } from "lodash";
import React from "react";
import { Section, Select, Input, InputNumber, Switch} from "@/components/visualizations/editor";
import { EditorPropTypes } from "@/visualizations/prop-types";



export default function GeneralSettings({options, data, visualizationName, onOptionsChange}: any) {
    return (
        <React.Fragment>
            {/* @ts-expect-error ts-migrate(2745) FIXME: This JSX tag's 'children' prop expects type 'never... Remove this comment to see the full error message */}
            <Section>
                <Input
                    layout="horizontal"
                    label="Counter Label"
                    data-test="Counter.General.Label"
                    defaultValue={options.counterLabel}
                    placeholder={visualizationName}
                    onChange={(e: any) => onOptionsChange({ counterLabel: e.target.value })}
                />
            </Section>
        </React.Fragment>
    )
}


GeneralSettings.prototype = EditorPropTypes;