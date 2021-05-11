import qs, { ParsedUrlQueryInput } from 'querystring';
import { useEffect, useState } from 'react';
import { API_URL } from "../../../utils/constants";

interface UseBuildResult {
  loading: boolean;
  data: any;
  rowCount: number;
  fetchData: (params: ParsedUrlQueryInput, rowsPerPage: number, offset: number) => void;
  getNext?: () => void;
  getPrev?: () => void;
}

const useBuild = (repoId: number): UseBuildResult => {
  const URL_BASE = `${API_URL}/repos/${repoId}/builds`;
  const [loading, setLoading] = useState(false);
  const [rowCount, setRowCount] = useState(0);
  const [build, setBuild] = useState<any>([]);
  let next, prev;

  const fetchBuild = (url?: string) => {
    if (!url) {
      return;
    }

    setLoading(true);
    fetch(url)
      .then(resp => resp.json())
      .then((json: any) => {
        // setBuild([...build, ...json.results]);
        setBuild(json.results);
        setRowCount(json.count);
        next = () => { fetchBuild(json.next) };
        prev = () => { fetchBuild(json.previous) };
        setLoading(false);
      });
  };

  // useEffect(() => {
  //   fetchBuild(
  //     params.url as string || `${URL_BASE}?${qs.stringify({...params, limit: rowsPerPage, offset})}`
  //   )
  // }, []);
  
  return {
    loading,
    data: build,
    rowCount,
    fetchData: (params: ParsedUrlQueryInput, rowsPerPage: number, offset: number) => {
      fetchBuild(`${URL_BASE}?${qs.stringify({...params, limit: rowsPerPage, offset})}`);
    },
    getNext: next,
    getPrev: prev,
  }
}

export default useBuild;