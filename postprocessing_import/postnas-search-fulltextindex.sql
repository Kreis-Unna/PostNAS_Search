BEGIN;
	/* alte Einträge löschen */
	DELETE FROM postnas_search;
	
	/* aktuelle Flurstücke verarbeiten */
	INSERT INTO postnas_search (
	SELECT ax_flurstueck.gml_id,
		to_tsvector('german'::regconfig, 
			/* Mit leerzeichen getrennt */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE ax_flurstueck.zaehler END || ' ' ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' ||
			/* Ohne leerzeichen getrennt ohne führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE ax_flurstueck.zaehler END ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' ||
			/* Ohne leerzeichen getrennt mit führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' ||
			/* Mit Trennzeichen - ohne führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE ax_flurstueck.zaehler END || '-' ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' ||
			/* Mit Trennzeichen - mit führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' ||
			/* Gemarkungsname */
			CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END)
	FROM ax_flurstueck 
	JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL
	WHERE ax_flurstueck.endet IS NULL);
	
	/* historische Flurstücke verarbeiten */
	INSERT INTO postnas_search (
		SELECT ax_historischesflurstueck.gml_id,
			to_tsvector('german'::regconfig,
				/* Mit leerzeichen getrennt */
				CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' ||
				CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' ||
				CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || ' ' ||
				CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' ||
				/* Ohne leerzeichen getrennt ohne führende Nullen */
				CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END ||
				CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END ||
				CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END ||
				CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' ||
				/* Ohne leerzeichen getrennt mit führende Nullen */
				CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END ||
				CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END ||
				CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END ||
				CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' ||
				/* Mit Trennzeichen - ohne führende Nullen */
				CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' ||
				CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' ||
				CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || '-' ||
				CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' ||
				/* Mit Trennzeichen - mit führende Nullen */
				CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' ||
				CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' ||
				CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' ||
				CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' ||
				/* Gemarkungsname */
				CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END
			)
		FROM ax_historischesflurstueck 
	JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL
	WHERE ax_historischesflurstueck.endet IS NULL);
COMMIT;