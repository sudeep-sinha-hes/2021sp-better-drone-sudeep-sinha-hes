import React, { FC } from 'react';
import PropTypes from 'prop-types';

import TablePagination from '@material-ui/core/TablePagination';

import IconButton from '@material-ui/core/IconButton';
import FirstPageIcon from '@material-ui/icons/FirstPage';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import LastPageIcon from '@material-ui/icons/LastPage';

type TablePaginationActionsProps = {
  count: number;
  page: number;
  rowsPerPage: number;
  onChangePage: (page: number) => void;
}

const TablePaginationActions: FC<TablePaginationActionsProps> = ({ count, page, rowsPerPage, onChangePage }) => {
  const getNumberOfPages = (c: number, r: number) => Math.ceil(c/r);

	const handleFirstPageButtonClick = () => {
		onChangePage(1);
	};

	// RDT uses page index starting at 1, MUI starts at 0
	// i.e. page prop will be off by one here
	const handleBackButtonClick = () => {
		onChangePage(page);
	};

	const handleNextButtonClick = () => {
		onChangePage(page + 2);
	};

	const handleLastPageButtonClick = () => {
		onChangePage(getNumberOfPages(count, rowsPerPage));
	};

	return (
		<>
			<IconButton onClick={handleFirstPageButtonClick} disabled={page === 0} aria-label="first page">
				<FirstPageIcon />
			</IconButton>
			<IconButton onClick={handleBackButtonClick} disabled={page === 0} aria-label="previous page">
				<KeyboardArrowLeft />
			</IconButton>
			<IconButton
				onClick={handleNextButtonClick}
				disabled={page >= getNumberOfPages(count, rowsPerPage) - 1}
				aria-label="next page"
			>
				<KeyboardArrowRight />
			</IconButton>
			<IconButton
				onClick={handleLastPageButtonClick}
				disabled={page >= getNumberOfPages(count, rowsPerPage) - 1}
				aria-label="last page"
			>
				<LastPageIcon />
			</IconButton>
		</>
	);
}


type CustomMaterialPaginationProps = {
  rowCount: number;
  page: number;
  rowsPerPage: number;
  currentPage: number;
  onChangePage: (page: number) => void;
  onChangeRowsPerPage: (rows: number) => void;
};

const CustomMaterialPagination: FC<CustomMaterialPaginationProps> = ({ rowsPerPage, rowCount, onChangePage, onChangeRowsPerPage, currentPage }) => (
  // @ts-ignore
	<TablePagination
		component="nav"
		count={rowCount}
		rowsPerPage={rowsPerPage}
		page={currentPage - 1}
		onChangePage={onChangePage}
		onChangeRowsPerPage={({ target }) => onChangeRowsPerPage(Number(target.value))}
		ActionsComponent={TablePaginationActions}
	/>
);

export default CustomMaterialPagination;