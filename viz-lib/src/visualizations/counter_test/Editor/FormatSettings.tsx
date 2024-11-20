import React from "react"
import {Section, Input, InputNumber, Switch} from "@/components/visualizations/editor";
import { EditorPropTypes } from "@/visualizations/prop-types";

import { isValueNumber } from "../utils";



export default function FormatSettings({ options, data, onOptionsChange }: any) {
    const inputsEnabled = isValueNumber(data.rows, options);

    return (
        <React.Fragment>
            {/* @ts-expect-error ts-migrate(2745) FIXME: This JSX tag's 'children' prop expects type 'never... Remove this comment to see the full error message */}
            <Section>
                <InputNumber
                    layout="horizontal"
                    label="Format Decimal Place"
                    data-test="Counter.Formatting.DecimalPlace"
                    defaultValue={options.stringDecimal}
                    disabled={!inputsEnabled}
                    onChange={(stringDecimal: any) => onOptionsChange({stringDecimal})}
                    />
            </Section>

            {/* @ts-expect-error ts-migrate(2745) FIXME: This JSX tag's 'children' prop expects type 'never... Remove this comment to see the full error message */}
            <Section>
                <Input
                layout="horizontal"
                label="Formatting Decimal Character"
                data-test="Counter.Formatting.DecimalCharacter"
                defaultValue={options.stringDecChar}
                disabled={!inputsEnabled}
                onChange={(e: any) => onOptionsChange({ stringDecChar: e.target.value })}
                />
            </Section>
        </React.Fragment>
    );
}

FormatSettings.prototype = EditorPropTypes