import React, { PureComponent } from 'react';
import { Row, Col, Select } from 'antd';

import styles from './GeomConfigPanel.less';

const Option = Select.Option;

class GeomConfigPanel extends PureComponent {
  render() {
    const { geomKey, cols, handleUpdate , geomValues} = this.props;
    const fields = [];
    if (cols) {
      cols.map(col => fields.push(col.key));
    }

    const fieldsList = fields.map(value => {
      return <Option key={value}>{value}</Option>;
    });

    const geomTypeListStr = [
      'point',
      'path',
      'line',
      'area',
      'interval',
      'polygon',
      'schema',
      'edge',
      'heatmap',
    ];
    const geomTypeList = geomTypeListStr.map(value => {
      return <Option key={value}>{value}</Option>;
    });

    const geomAttributes = ['position', 'color', 'size', 'shape', 'opacity', 'label'];

    const buildSelect = (type, children, single, selected) => {
      const hint = `please select ${type}`;
      const handleChange = value => {
        handleUpdate(type, value, geomKey);
      };
      return (
        <Select
          showSearch
          mode={single ? '' : 'tags'}
          placeholder={hint}
          onChange={handleChange}
          style={{ width: '100%' }}
          value={selected}
        >
          {children}
        </Select>
      );
    };

    const geomTypeSelected = (geomValues && geomValues.geometry) ? geomValues.geometry:[];
    const geomTypeSelector = buildSelect('geometry', geomTypeList, true, geomTypeSelected);

    const geomAttributesSelectors = geomAttributes.map(attr => {
      const selected = (geomValues && geomValues[attr]) ? geomValues[attr]:[];
      const content = buildSelect(attr, fieldsList, false, selected);
      return (
        <li key={attr}>
          {attr}:{content}
        </li>
      );
    });

    return (
      <div className={styles.geomConfigPanel}>
        geometry:
        {geomTypeSelector}
        {geomAttributesSelectors}
      </div>
    );
  }
}

export default GeomConfigPanel;