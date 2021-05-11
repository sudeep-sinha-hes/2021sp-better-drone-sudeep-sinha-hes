import { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core';
import LinearProgress from '@material-ui/core/LinearProgress';
import DataTable, { IDataTableColumn } from 'react-data-table-component';

import useBuild from './useBuild';
import CustomMaterialPagination from './PaginationComponent';


const useStyles = makeStyles(theme => ({
  root: {
    width: '100%',
    '& > * + *': {
      marginTop: theme.spacing(2),
    },
  },
}));

const LinearIndeterminate = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <LinearProgress />
    </div>
  );
};


const columns: IDataTableColumn[] = [
  {
    selector: "id",
    name: "Id",
    maxWidth: '100px',
  },
  {
    selector: "author_email",
    name: "Author",
    sortable: true,
  },
  {
    selector: "event",
    name: "Event Type",
  },
  {
    selector: "deploy_to",
    name: "Target Env",
  },
  {
    selector: "status",
    name: "Status",
  },
  {
    selector: "started",
    name: "Start Time",
    sortable: true,
  },
  {
    selector: "finished",
    name: "End Time",
    sortable: true,
  }
];

const conditionalRowStyles = [
  {
    when: (row: any) => row.status === 'success',
    style: {
      borderLeft: '3px solid rgba(63, 195, 128, 0.9)',
      cursor: 'pointer'
    },
  },
  {
    when: (row: any) => row.status !== 'success',
    style: {
      borderLeft: '3px solid rgba(242, 38, 19, 0.9)',
      cursor: 'pointer'
    },
  },
];

const BuildTable = ({ repoId }: {repoId: number}) => {
  const [params, setParams] = useState({});
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [offset, setOffset] = useState(0);
  const { loading, data: fetchedData, fetchData, getNext, getPrev, rowCount } = useBuild(repoId);

  const handleChangeRowsPerPage = (rows: number) => {
    setRowsPerPage(rows);
    fetchData(params, rows, offset);
  }

  const handlePageChange = (page: number) => {
    setOffset(page * rowsPerPage);
    fetchData(params, rowsPerPage, page * rowsPerPage);
  };  

  useEffect(() => {
    fetchData(params, rowsPerPage, offset);
  }, [])

  return (
    <DataTable
      title="Builds"
      columns={columns}
      data={fetchedData}
      conditionalRowStyles={conditionalRowStyles}
      progressPending={loading}
      progressComponent={<LinearIndeterminate />}
      persistTableHead
      pagination
		  paginationComponent={CustomMaterialPagination}
      paginationTotalRows={rowCount}
      paginationPerPage={rowsPerPage}
      onChangePage={handlePageChange}
      onChangeRowsPerPage={handleChangeRowsPerPage}
    />
  );
}

export default BuildTable;