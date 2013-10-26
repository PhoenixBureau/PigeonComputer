def make_lambda_ast(variables, exp, context):
  variables = tuple(v.data for v in variables.data)
  exp = list_(*exp.data)

  def inner(*args):
    new_context = send(context, 'delegated')
    for k, v in zip(variables, args):
      send(new_context, 'addMethod', k, v)
    return evaluate(exp, new_context)

  return inner


def evaluate(ast, context):
  symbol = send(ast, 'typeOf')
  sname = send(symbol, 'getName')

  if sname == 'symbol':
    try:
      return send(context, 'lookup', ast.data)
    except:
      return ast.data

  if sname == 'literal':
    return ast.data

  first, rest = ast.data[0], ast.data[1:]
  symbol = send(first, 'typeOf')
  sname = send(symbol, 'getName')

  if sname == 'symbol':

    if first.data == 'define':
      var, exp = rest
      var = var.data
      value = evaluate(exp, context)
      send(context, 'addMethod', var, value)
      return

    elif first.data == 'lambda':
      variables, exp = rest
      return make_lambda_ast(variables, exp, context)

  exp = tuple(evaluate(it, context) for it in ast.data)
  if callable(exp[0]):
    return exp[0](*exp[1:])

  return exp

def evaluate_list(ast, context):
  print '<', evaluate(ast, context), '>'


