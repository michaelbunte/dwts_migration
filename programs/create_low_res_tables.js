async function populate_low_res(
    postgresClient,
    plc_table_name,
    low_res_plc_table_name
) {

    // https://stackoverflow.com/questions/1050720/how-to-add-hours-to-a-date-object
    function addhours(date, h) {
        date.setTime(date.getTime() + (h * 60 * 60 * 1000));
        return date;
    }
    const get_earliest_date = `
        SELECT plctime FROM ${plc_table_name} ORDER BY plctime ASC LIMIT 1;
    `;

    let first_date = undefined;
    try {
        const result = await postgresClient.query(get_earliest_date);
        first_date = result.rows[0].plctime;
    } catch (err) {
        console.error(err);
        throw err;
    }

    let current_date = first_date;
    for (let i = 0; ; i++) {
        try {
            const result = await postgresClient.query(
                `
                SELECT *
                FROM ${plc_table_name}
                WHERE plctime >= '${current_date.toISOString()}'
                ORDER BY plctime ASC LIMIT 1 ;
                `
            );
            if (result.rows[0].length === 0) {
                return;
            }
        } catch (err) {
            console.error(err);
            return;
        }

        console.log(i);
        const insert_string = `
            INSERT INTO ${low_res_plc_table_name}
            SELECT *
            FROM ${plc_table_name}
            WHERE plctime >= '${current_date.toISOString()}'
            ORDER BY plctime ASC LIMIT 1 ;
        `;

        await postgresClient.query(insert_string);
        current_date = addhours(current_date, 6);
    }
}