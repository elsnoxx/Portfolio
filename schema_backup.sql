--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8 (Debian 15.8-0+deb12u1)
-- Dumped by pg_dump version 15.8 (Debian 15.8-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: calculate_portfolio(); Type: FUNCTION; Schema: public; Owner: su
--

CREATE FUNCTION public.calculate_portfolio() RETURNS TABLE(ticker character varying, total_investment numeric, total_units numeric, total_dividend numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        trades.details::VARCHAR AS ticker,  -- Převod na VARCHAR
        ROUND(SUM(CASE
            WHEN type = 'Open Position' THEN amount
            WHEN type = 'Position closed' THEN -amount
            ELSE 0
        END), 2) AS total_investment,  -- Zaokrouhlení na 2 desetinná místa
        ROUND(SUM(CASE
            WHEN type = 'Open Position' THEN units
            WHEN type = 'Position closed' THEN -units
            ELSE 0
        END), 2) AS total_units,  -- Zaokrouhlení na 2 desetinná místa
        COALESCE(ROUND(SUM(CASE
            WHEN d.total > 0 THEN d.total
            ELSE 0
        END), 2), 0) AS total_dividend  -- Celková dividenda, pokud je větší než 0
    FROM
        trades
    LEFT JOIN (
        SELECT details, SUM(amount) AS total
        FROM dividendy_portfolio  -- Použití nového názvu tabulky
        GROUP BY details
    ) AS d ON trades.details = d.details  -- Spojení s dividendami
    GROUP BY
        trades.details
    HAVING
        ROUND(SUM(CASE
            WHEN type = 'Open Position' THEN amount
            WHEN type = 'Position closed' THEN -amount
            ELSE 0
        END), 2) > 0 OR
        ROUND(SUM(CASE
            WHEN type = 'Open Position' THEN units
            WHEN type = 'Position closed' THEN -units
            ELSE 0
        END), 2) > 0;  -- Filtrujeme, abychom vrátili pouze hodnoty větší než 0
END;
$$;


ALTER FUNCTION public.calculate_portfolio() OWNER TO su;

--
-- Name: get_dividend_totals(); Type: FUNCTION; Schema: public; Owner: su
--

CREATE FUNCTION public.get_dividend_totals() RETURNS TABLE(details text, total numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT dividends.details, SUM(amount) AS total 
    FROM dividends 
    GROUP BY dividends.details;
END;
$$;


ALTER FUNCTION public.get_dividend_totals() OWNER TO su;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: companies; Type: TABLE; Schema: public; Owner: su
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    ticker character varying(10) NOT NULL,
    sector character varying(50),
    market_cap numeric(15,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.companies OWNER TO su;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: su
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_id_seq OWNER TO su;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: su
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Name: dividends; Type: TABLE; Schema: public; Owner: su
--

CREATE TABLE public.dividends (
    id integer NOT NULL,
    company_id integer,
    ex_date date NOT NULL,
    amount numeric(10,2) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.dividends OWNER TO su;

--
-- Name: dividends_id_seq; Type: SEQUENCE; Schema: public; Owner: su
--

CREATE SEQUENCE public.dividends_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dividends_id_seq OWNER TO su;

--
-- Name: dividends_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: su
--

ALTER SEQUENCE public.dividends_id_seq OWNED BY public.dividends.id;


--
-- Name: dividendy_portfolio; Type: TABLE; Schema: public; Owner: su
--

CREATE TABLE public.dividendy_portfolio (
    id integer NOT NULL,
    date date NOT NULL,
    type text NOT NULL,
    details text,
    amount numeric NOT NULL
);


ALTER TABLE public.dividendy_portfolio OWNER TO su;

--
-- Name: dividendy_portfolio_id_seq; Type: SEQUENCE; Schema: public; Owner: su
--

CREATE SEQUENCE public.dividendy_portfolio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dividendy_portfolio_id_seq OWNER TO su;

--
-- Name: dividendy_portfolio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: su
--

ALTER SEQUENCE public.dividendy_portfolio_id_seq OWNED BY public.dividendy_portfolio.id;


--
-- Name: financials; Type: TABLE; Schema: public; Owner: su
--

CREATE TABLE public.financials (
    id integer NOT NULL,
    company_id integer,
    year integer NOT NULL,
    revenue numeric(15,2),
    expenses numeric(15,2),
    net_income numeric(15,2),
    dividend numeric(15,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.financials OWNER TO su;

--
-- Name: financials_id_seq; Type: SEQUENCE; Schema: public; Owner: su
--

CREATE SEQUENCE public.financials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.financials_id_seq OWNER TO su;

--
-- Name: financials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: su
--

ALTER SEQUENCE public.financials_id_seq OWNED BY public.financials.id;


--
-- Name: historical_prices; Type: TABLE; Schema: public; Owner: su
--

CREATE TABLE public.historical_prices (
    id integer NOT NULL,
    company_id integer,
    date date NOT NULL,
    open_price numeric(10,2),
    close_price numeric(10,2),
    high_price numeric(10,2),
    low_price numeric(10,2),
    volume bigint,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.historical_prices OWNER TO su;

--
-- Name: historical_prices_id_seq; Type: SEQUENCE; Schema: public; Owner: su
--

CREATE SEQUENCE public.historical_prices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.historical_prices_id_seq OWNER TO su;

--
-- Name: historical_prices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: su
--

ALTER SEQUENCE public.historical_prices_id_seq OWNED BY public.historical_prices.id;


--
-- Name: trades; Type: TABLE; Schema: public; Owner: su
--

CREATE TABLE public.trades (
    id integer NOT NULL,
    date date NOT NULL,
    type text NOT NULL,
    details character varying,
    amount numeric NOT NULL,
    units numeric NOT NULL
);


ALTER TABLE public.trades OWNER TO su;

--
-- Name: trades_id_seq; Type: SEQUENCE; Schema: public; Owner: su
--

CREATE SEQUENCE public.trades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trades_id_seq OWNER TO su;

--
-- Name: trades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: su
--

ALTER SEQUENCE public.trades_id_seq OWNED BY public.trades.id;


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: dividends id; Type: DEFAULT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.dividends ALTER COLUMN id SET DEFAULT nextval('public.dividends_id_seq'::regclass);


--
-- Name: dividendy_portfolio id; Type: DEFAULT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.dividendy_portfolio ALTER COLUMN id SET DEFAULT nextval('public.dividendy_portfolio_id_seq'::regclass);


--
-- Name: financials id; Type: DEFAULT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.financials ALTER COLUMN id SET DEFAULT nextval('public.financials_id_seq'::regclass);


--
-- Name: historical_prices id; Type: DEFAULT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.historical_prices ALTER COLUMN id SET DEFAULT nextval('public.historical_prices_id_seq'::regclass);


--
-- Name: trades id; Type: DEFAULT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.trades ALTER COLUMN id SET DEFAULT nextval('public.trades_id_seq'::regclass);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: companies companies_ticker_key; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_ticker_key UNIQUE (ticker);


--
-- Name: dividends dividends_pkey; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.dividends
    ADD CONSTRAINT dividends_pkey PRIMARY KEY (id);


--
-- Name: dividendy_portfolio dividendy_portfolio_pkey; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.dividendy_portfolio
    ADD CONSTRAINT dividendy_portfolio_pkey PRIMARY KEY (id);


--
-- Name: financials financials_company_id_year_key; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.financials
    ADD CONSTRAINT financials_company_id_year_key UNIQUE (company_id, year);


--
-- Name: financials financials_pkey; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.financials
    ADD CONSTRAINT financials_pkey PRIMARY KEY (id);


--
-- Name: historical_prices historical_prices_company_id_date_key; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.historical_prices
    ADD CONSTRAINT historical_prices_company_id_date_key UNIQUE (company_id, date);


--
-- Name: historical_prices historical_prices_pkey; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.historical_prices
    ADD CONSTRAINT historical_prices_pkey PRIMARY KEY (id);


--
-- Name: trades trades_pkey; Type: CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_pkey PRIMARY KEY (id);


--
-- Name: dividends dividends_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.dividends
    ADD CONSTRAINT dividends_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;


--
-- Name: financials financials_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.financials
    ADD CONSTRAINT financials_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;


--
-- Name: historical_prices historical_prices_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: su
--

ALTER TABLE ONLY public.historical_prices
    ADD CONSTRAINT historical_prices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

