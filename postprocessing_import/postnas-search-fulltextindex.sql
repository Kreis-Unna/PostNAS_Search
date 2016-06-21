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
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' ||
			/* Ohne leerzeichen getrennt ohne führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' ||
			/* Ohne leerzeichen getrennt mit führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END ||
			CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' ||
			/* Mit Trennzeichen - ohne führende Nullen */
			CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' ||
			CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' ||
			CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' ||
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
	
	/* historische Flurstücke ohne Raumbezug verarbeiten */
	INSERT INTO postnas_search (
		SELECT ax_historischesflurstueckohneraumbezug.gml_id,
			to_tsvector('german'::regconfig,
				/* Mit leerzeichen getrennt */
				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' ||
				/* Ohne leerzeichen getrennt ohne führende Nullen */
				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' ||
				/* Ohne leerzeichen getrennt mit führende Nullen */
				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' ||
				/* Mit Trennzeichen - ohne führende Nullen */
				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' ||
				/* Mit Trennzeichen - mit führende Nullen */
				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' ||
				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' ||
				/* Gemarkungsname */
				CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END
			)
		FROM ax_historischesflurstueckohneraumbezug 
	JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL
	WHERE ax_historischesflurstueckohneraumbezug.endet IS NULL);
	
	/* Straßennamen */
	INSERT INTO postnas_search (
		SELECT 
			ax_lagebezeichnungmithausnummer.gml_id,
			to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || reverse(ax_lagebezeichnungkatalogeintrag.bezeichnung::text) || ' ' || ax_lagebezeichnungmithausnummer.hausnummer || ' ' || ax_gemeinde.bezeichnung)
		FROM ax_lagebezeichnungkatalogeintrag
		JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL
		JOIN ax_lagebezeichnungmithausnummer ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage AND ax_lagebezeichnungmithausnummer.endet IS NULL
		WHERE ax_lagebezeichnungkatalogeintrag.endet IS NULL
	);
	
	/* Eigentümer */
	INSERT INTO postnas_search (
		SELECT 
			gml_id,
			to_tsvector('german',CASE WHEN nachnameoderfirma IS NOT NULL THEN nachnameoderfirma || ' ' || reverse(nachnameoderfirma) || ' ' ELSE '' END || CASE WHEN vorname IS NOT NULL THEN vorname || ' ' || reverse(vorname) || ' ' ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname || ' ' || reverse(geburtsname) ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil || ' ' || reverse(namensbestandteil) ELSE '' END || CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad || ' ' || reverse(akademischergrad) ELSE '' END) 
		FROM ax_person 
		WHERE endet IS NULL
	);
COMMIT;