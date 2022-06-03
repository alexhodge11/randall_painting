function calculateTotal()
  {
  let tax_percent = 1.27

  let total = tax_percent * (parseFloat($("#labor_cost").val()?$("#labor_cost").val():"0") + parseFloat($("#supplies_cost").val()?$("#supplies_cost").val():"0"));

  let tax_total = 0.27 * (parseFloat($("#labor_cost").val()?$("#labor_cost").val():"0") + parseFloat($("#supplies_cost").val()?$("#supplies_cost").val():"0"));

  $("#grand_total").text(format_currency(total));

  $("#tax").text(format_currency(tax_total));

}

$(".cost").keyup(calculateTotal)

function round(num) {
  return Math.round((num + Number.EPSILON) * 100) / 100
}

function format_currency(num) {
  let formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  });
  return formatter.format(num)
}